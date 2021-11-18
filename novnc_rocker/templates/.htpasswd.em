@{import bcrypt}@
@(novnc_user):@(bcrypt.hashpw(novnc_password.encode('utf8'), bcrypt.gensalt(rounds=10)).decode())
