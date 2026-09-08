-- =============================================================
-- 项目：基于LangChain的带AI智能客服的微信小程序商城系统
-- 数据库：MySQL 8.x（端口 3306）
-- 字符集：utf8mb4
-- 说明：本文件为建表语句
-- =============================================================

-- 创建数据库（若不存在）
CREATE DATABASE IF NOT EXISTS `shop_agent`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE `shop_agent`;

-- 删除旧表（按依赖顺序，便于重复执行）
DROP TABLE IF EXISTS `chat_message`;
DROP TABLE IF EXISTS `knowledge_file`;
DROP TABLE IF EXISTS `order_item`;
DROP TABLE IF EXISTS `order`;
DROP TABLE IF EXISTS `cart`;
DROP TABLE IF EXISTS `address`;
DROP TABLE IF EXISTS `product`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `user`;

-- -------------------------------------------------------------
-- 用户表：普通用户与管理员共用，role 区分（0=普通用户 1=管理员）
-- 密码使用 MD5 加密存储（测试密码 123456）
-- -------------------------------------------------------------
CREATE TABLE `user` (
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username`    VARCHAR(64)  NOT NULL COMMENT '登录账号',
    `password`    VARCHAR(64)  NOT NULL COMMENT '密码(MD5)',
    `nickname`    VARCHAR(64)  DEFAULT NULL COMMENT '昵称',
    `avatar`      VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    `phone`       VARCHAR(20)  DEFAULT NULL COMMENT '手机号',
    `email`       VARCHAR(128) DEFAULT NULL COMMENT '邮箱',
    `role`        TINYINT      NOT NULL DEFAULT 0 COMMENT '角色：0=普通用户 1=管理员',
    `status`      TINYINT      NOT NULL DEFAULT 1 COMMENT '状态：0=禁用 1=正常',
    `created_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '用户表';

-- -------------------------------------------------------------
-- 商品分类表
-- -------------------------------------------------------------
CREATE TABLE `category` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
    `name`       VARCHAR(64) NOT NULL COMMENT '分类名称',
    `sort`       INT         NOT NULL DEFAULT 0 COMMENT '排序（越大越靠前）',
    `status`     TINYINT     NOT NULL DEFAULT 1 COMMENT '状态：0=停用 1=启用',
    `created_at` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '商品分类表';

-- -------------------------------------------------------------
-- 商品表
-- -------------------------------------------------------------
CREATE TABLE `product` (
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '商品ID',
    `category_id`   BIGINT UNSIGNED NOT NULL COMMENT '所属分类ID',
    `name`          VARCHAR(128)   NOT NULL COMMENT '商品名称',
    `description`   TEXT           DEFAULT NULL COMMENT '商品描述',
    `price`         DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '售价',
    `original_price` DECIMAL(10, 2) DEFAULT NULL COMMENT '原价',
    `stock`         INT            NOT NULL DEFAULT 0 COMMENT '库存',
    `sales`         INT            NOT NULL DEFAULT 0 COMMENT '销量',
    `cover_image`   VARCHAR(255)   DEFAULT NULL COMMENT '封面图URL',
    `images`        TEXT           DEFAULT NULL COMMENT '轮播图URL列表(JSON)',
    `status`        TINYINT        NOT NULL DEFAULT 1 COMMENT '状态：0=下架 1=上架',
    `created_at`    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at`    DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_category_id` (`category_id`),
    CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '商品表';

-- -------------------------------------------------------------
-- 收货地址表
-- -------------------------------------------------------------
CREATE TABLE `address` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '地址ID',
    `user_id`    BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `name`       VARCHAR(64)  NOT NULL COMMENT '收货人姓名',
    `phone`      VARCHAR(20)  NOT NULL COMMENT '收货人电话',
    `province`   VARCHAR(64)  DEFAULT NULL COMMENT '省',
    `city`       VARCHAR(64)  DEFAULT NULL COMMENT '市',
    `district`   VARCHAR(64)  DEFAULT NULL COMMENT '区',
    `detail`     VARCHAR(255) NOT NULL COMMENT '详细地址',
    `is_default` TINYINT      NOT NULL DEFAULT 0 COMMENT '是否默认：0=否 1=是',
    `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '收货地址表';

-- -------------------------------------------------------------
-- 购物车表
-- -------------------------------------------------------------
CREATE TABLE `cart` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '购物车项ID',
    `user_id`    BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    `product_id` BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    `quantity`   INT            NOT NULL DEFAULT 1 COMMENT '数量',
    `created_at` DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_user_product` (`user_id`, `product_id`),
    KEY `idx_product_id` (`product_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '购物车表';

-- -------------------------------------------------------------
-- 订单表
-- -------------------------------------------------------------
CREATE TABLE `order` (
    `id`           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '订单ID',
    `order_no`     VARCHAR(64)   NOT NULL COMMENT '订单号',
    `user_id`      BIGINT UNSIGNED NOT NULL COMMENT '下单用户ID',
    `total_amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '订单总金额',
    `status`       TINYINT       NOT NULL DEFAULT 0 COMMENT '状态：0=待付款 1=待发货 2=待收货 3=已完成 4=已取消',
    `address_id`   BIGINT UNSIGNED DEFAULT NULL COMMENT '收货地址ID',
    `remark`       VARCHAR(255)  DEFAULT NULL COMMENT '买家备注',
    `created_at`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下单时间',
    `updated_at`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_order_no` (`order_no`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_created_at` (`created_at`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '订单表';

-- -------------------------------------------------------------
-- 订单明细表
-- -------------------------------------------------------------
CREATE TABLE `order_item` (
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '明细ID',
    `order_id`      BIGINT UNSIGNED NOT NULL COMMENT '订单ID',
    `product_id`    BIGINT UNSIGNED NOT NULL COMMENT '商品ID',
    `product_name`  VARCHAR(128)   NOT NULL COMMENT '商品名称(快照)',
    `product_image` VARCHAR(255)   DEFAULT NULL COMMENT '商品图片(快照)',
    `price`         DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '成交单价',
    `quantity`      INT            NOT NULL DEFAULT 1 COMMENT '购买数量',
    PRIMARY KEY (`id`),
    KEY `idx_order_id` (`order_id`),
    CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '订单明细表';

-- -------------------------------------------------------------
-- 知识库文件表：记录上传的知识库文档及其向量化状态
-- -------------------------------------------------------------
CREATE TABLE `knowledge_file` (
    `id`           BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '文件ID',
    `filename`     VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `file_type`    VARCHAR(16)  NOT NULL COMMENT '文件类型：txt/doc/pdf/markdown',
    `file_path`    VARCHAR(500) NOT NULL COMMENT '本地存储路径',
    `size`         INT          NOT NULL DEFAULT 0 COMMENT '文件大小(字节)',
    `status`       TINYINT      NOT NULL DEFAULT 0 COMMENT '状态：0=待处理 1=已向量化 2=处理失败',
    `chunk_count`  INT          NOT NULL DEFAULT 0 COMMENT '切分文本块数量',
    `error_msg`    VARCHAR(500) DEFAULT NULL COMMENT '失败原因',
    `created_at`   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '知识库文件表';

-- -------------------------------------------------------------
-- 聊天记录表：记录 AI 客服对话历史
-- -------------------------------------------------------------
CREATE TABLE `chat_message` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '消息ID',
    `user_id`    BIGINT UNSIGNED DEFAULT NULL COMMENT '用户ID(游客为NULL)',
    `session_id` VARCHAR(64)  NOT NULL COMMENT '会话ID',
    `role`       VARCHAR(16)  NOT NULL COMMENT '角色：user/assistant',
    `content`    TEXT         NOT NULL COMMENT '消息内容',
    `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发送时间',
    PRIMARY KEY (`id`),
    KEY `idx_session_id` (`session_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '聊天记录表';

-- -------------------------------------------------------------
-- 轮播图表：小程序首页顶部轮播，后台维护
-- -------------------------------------------------------------
CREATE TABLE `banner` (
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '轮播图ID',
    `title`      VARCHAR(128) DEFAULT NULL COMMENT '标题',
    `image`      VARCHAR(255) NOT NULL COMMENT '图片URL',
    `sort`       INT         NOT NULL DEFAULT 0 COMMENT '排序(越大越靠前)',
    `status`     SMALLINT    NOT NULL DEFAULT 1 COMMENT '0=停用 1=启用',
    `created_at` DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT = '轮播图表';
