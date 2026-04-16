const express = require("express");
const router = express.Router();

const { login, register, dashboard, getAllUsers, logout } = require("../controllers/user");
const authMiddleware = require('../middleware/auth')

router.route("/login").post(login);
router.route("/register").post(register);
router.route("/logout").post(authMiddleware, logout);
router.route("/dashboard").get(authMiddleware, dashboard);
router.route("/users").get(getAllUsers);


module.exports = router;