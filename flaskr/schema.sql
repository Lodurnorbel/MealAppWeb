DROP TABLE IF EXISTS userRoles;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS meal;

CREATE TABLE IF NOT EXISTS userRoles(
    'id' INTEGER PRIMARY KEY,
    'name' varchar(10) NOT NULL,
    'canEdit' varchar(50) NOT NULL,
    'canAdd' int NOT NULL,
    'canDelete' int NOT NULL
);

CREATE TABLE IF NOT EXISTS user(
    'id' INTEGER PRIMARY KEY,
    'username' varchar(10) NOT NULL UNIQUE,
    'password' varchar(50) NOT NULL,
    'roleId' INTEGER,
    FOREIGN KEY (roleId)
        REFERENCES userRoles (id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS meal(
    'id' INTEGER PRIMARY KEY,
    'name' VARCHAR(50),
    'onMenu' INTEGER,
    'price' REAL,
    'updateDate' TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    'updateUser' INTEGER,
    'code' VARCHAR(50) NOT NULL,
    FOREIGN KEY (updateUser)
        REFERENCES user (id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
)