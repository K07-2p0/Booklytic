const jwt = require('jsonwebtoken');

const authenticationMiddleware = async (req, res, next) => {
  // Check for token in cookies first, then Authorization header
  let token = req.cookies?.token;

  if (!token) {
    const authHeader = req.headers.authorization
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({msg: "Unauthorized. Please add valid token"});
    }
    token = authHeader.split(' ')[1]
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET)
    const { id, name } = decoded
    req.user = { id, name }
    next()
  } catch (error) {
    return res.status(401).json({msg: "Unauthorized. Please add valid token"});
  }
}

module.exports = authenticationMiddleware