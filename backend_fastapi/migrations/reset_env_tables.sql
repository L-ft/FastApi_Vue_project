-- 首先删除相关的外键约束
SET FOREIGN_KEY_CHECKS = 0;

-- 删除已存在的表（按照依赖关系的顺序）
DROP TABLE IF EXISTS environment_variables;
DROP TABLE IF EXISTS api_info;
DROP TABLE IF EXISTS environments;

-- 重新启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 创建环境表
CREATE TABLE environments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    value VARCHAR(500) NOT NULL,
    description VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建环境变量表
CREATE TABLE environment_variables (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    env_id INTEGER NOT NULL,
    `key` VARCHAR(50) NOT NULL,
    value VARCHAR(500) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (env_id) REFERENCES environments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_env_key (env_id, `key`)
);

-- 创建或修改 api_info 表
CREATE TABLE IF NOT EXISTS api_info (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    group_id INTEGER,
    env_id INTEGER,
    description VARCHAR(255),
    FOREIGN KEY (env_id) REFERENCES environments(id) ON DELETE SET NULL,
    FOREIGN KEY (group_id) REFERENCES api_group(id) ON DELETE SET NULL
);
