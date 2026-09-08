-- =============================================================
-- 测试数据
-- 说明：所有用户密码统一为 123456，其 bcrypt 哈希值为 $2b$12$qajQgdEjl9PhJdttkrSvju4BgKDY4S1B1ETHQIN2Gik3H5pLXg/xm
-- =============================================================

USE `shop_agent`;

-- ------------------------- 用户 -------------------------
-- 管理员账号 admin / 123456
INSERT INTO `user` (`id`, `username`, `password`, `nickname`, `avatar`, `phone`, `email`, `role`, `status`) VALUES
(1, 'admin', '$2b$12$qajQgdEjl9PhJdttkrSvju4BgKDY4S1B1ETHQIN2Gik3H5pLXg/xm', '系统管理员', NULL, '13800000000', 'admin@shop.com', 1, 1),
(2, 'zhangsan', '$2b$12$qajQgdEjl9PhJdttkrSvju4BgKDY4S1B1ETHQIN2Gik3H5pLXg/xm', '张三', NULL, '13800000001', 'zhangsan@qq.com', 0, 1),
(3, 'lisi', '$2b$12$qajQgdEjl9PhJdttkrSvju4BgKDY4S1B1ETHQIN2Gik3H5pLXg/xm', '李四', NULL, '13800000002', 'lisi@qq.com', 0, 1),
(4, 'wangwu', '$2b$12$qajQgdEjl9PhJdttkrSvju4BgKDY4S1B1ETHQIN2Gik3H5pLXg/xm', '王五', NULL, '13800000003', 'wangwu@qq.com', 0, 1);

-- ------------------------- 分类 -------------------------
INSERT INTO `category` (`id`, `name`, `sort`, `status`) VALUES
(1, '手机数码', 100, 1),
(2, '家用电器', 90, 1),
(3, '服饰鞋包', 80, 1),
(4, '食品生鲜', 70, 1);

-- ------------------------- 商品 -------------------------
INSERT INTO `product` (`id`, `category_id`, `name`, `description`, `price`, `original_price`, `stock`, `sales`, `cover_image`, `images`, `status`) VALUES
(1, 1, '智能手机 Pro Max', '6.7英寸全面屏，旗舰级影像系统，支持5G', 6999.00, 7999.00, 120, 356, '/uploads14/product/phone.jpg', '["/uploads14/product/phone1.jpg","/uploads14/product/phone2.jpg"]', 1),
(2, 1, '无线降噪耳机', '主动降噪，超长续航40小时', 899.00, 1299.00, 300, 1024, '/uploads14/product/earphone.jpg', '["/uploads14/product/earphone1.jpg"]', 1),
(3, 1, '智能手表', '血氧心率监测，50米防水', 1599.00, 1899.00, 200, 512, '/uploads14/product/watch.jpg', '["/uploads14/product/watch1.jpg"]', 1),
(4, 2, '变频空调 1.5匹', '一级能效，快速冷暖', 2599.00, 3199.00, 80, 156, '/uploads14/product/aircon.jpg', '["/uploads14/product/aircon1.jpg"]', 1),
(5, 2, '滚筒洗衣机 10KG', '变频电机，高温除菌', 2999.00, 3599.00, 60, 89, '/uploads14/product/washer.jpg', '["/uploads14/product/washer1.jpg"]', 1),
(6, 2, '智能冰箱 三门', '风冷无霜，节能静音', 3499.00, 4299.00, 45, 67, '/uploads14/product/fridge.jpg', '["/uploads14/product/fridge1.jpg"]', 1),
(7, 3, '休闲运动鞋', '轻便透气，缓震舒适', 399.00, 599.00, 500, 2034, '/uploads14/product/shoes.jpg', '["/uploads14/product/shoes1.jpg"]', 1),
(8, 3, '纯棉T恤', '100%纯棉，舒适透气', 99.00, 159.00, 1000, 3456, '/uploads14/product/tshirt.jpg', '["/uploads14/product/tshirt1.jpg"]', 1),
(9, 4, '有机牛奶 250ml*12', '优质奶源，营养丰富', 59.90, 79.90, 800, 5678, '/uploads14/product/milk.jpg', '["/uploads14/product/milk1.jpg"]', 1),
(10, 4, '新鲜红富士苹果 5斤', '脆甜多汁，产地直发', 29.90, 39.90, 1500, 7890, '/uploads14/product/apple.jpg', '["/uploads14/product/apple1.jpg"]', 1);

-- ------------------------- 收货地址 -------------------------
INSERT INTO `address` (`id`, `user_id`, `name`, `phone`, `province`, `city`, `district`, `detail`, `is_default`) VALUES
(1, 2, '张三', '13800000001', '广东省', '深圳市', '南山区', '科技园路1号', 1),
(2, 3, '李四', '13800000002', '北京市', '北京市', '朝阳区', '望京街道2号', 1),
(3, 4, '王五', '13800000003', '上海市', '上海市', '浦东新区', '张江路3号', 1);

-- ------------------------- 购物车 -------------------------
INSERT INTO `cart` (`user_id`, `product_id`, `quantity`) VALUES
(2, 1, 1),
(2, 8, 2),
(3, 3, 1);

-- ------------------------- 订单（近7天，用于后台统计图表） -------------------------
INSERT INTO `order` (`id`, `order_no`, `user_id`, `total_amount`, `status`, `address_id`, `remark`, `created_at`) VALUES
(1, '202609010001', 2, 7898.00, 3, 1, '请尽快发货', '2026-09-01 10:23:45'),
(2, '202609020002', 3, 1599.00, 3, 2, NULL, '2026-09-02 14:11:20'),
(3, '202609030003', 4, 2999.00, 2, 3, NULL, '2026-09-03 09:45:33'),
(4, '202609040004', 2, 498.00, 1, 1, NULL, '2026-09-04 16:30:12'),
(5, '202609050005', 3, 3598.00, 0, 2, NULL, '2026-09-05 20:08:56'),
(6, '202609060006', 4, 89.80, 3, 3, NULL, '2026-09-06 11:22:47'),
(7, '202609070007', 2, 3499.00, 1, 1, '开发票', '2026-09-07 18:55:30'),
(8, '202609080008', 3, 1599.00, 4, 2, '买错了取消', '2026-09-08 08:40:15');

-- ------------------------- 订单明细 -------------------------
INSERT INTO `order_item` (`order_id`, `product_id`, `product_name`, `product_image`, `price`, `quantity`) VALUES
(1, 1, '智能手机 Pro Max', '/uploads14/product/phone.jpg', 6999.00, 1),
(1, 2, '无线降噪耳机', '/uploads14/product/earphone.jpg', 899.00, 1),
(2, 3, '智能手表', '/uploads14/product/watch.jpg', 1599.00, 1),
(3, 5, '滚筒洗衣机 10KG', '/uploads14/product/washer.jpg', 2999.00, 1),
(4, 8, '纯棉T恤', '/uploads14/product/tshirt.jpg', 99.00, 2),
(4, 7, '休闲运动鞋', '/uploads14/product/shoes.jpg', 399.00, 1),
(5, 3, '智能手表', '/uploads14/product/watch.jpg', 1599.00, 1),
(5, 2, '无线降噪耳机', '/uploads14/product/earphone.jpg', 899.00, 1),
(6, 10, '新鲜红富士苹果 5斤', '/uploads14/product/apple.jpg', 29.90, 3),
(7, 6, '智能冰箱 三门', '/uploads14/product/fridge.jpg', 3499.00, 1),
(8, 3, '智能手表', '/uploads14/product/watch.jpg', 1599.00, 1);

-- ------------------------- 首页轮播图 -------------------------
INSERT INTO `banner` (`title`, `image`, `sort`, `status`) VALUES
('新人特惠 纯牛奶包邮', '/uploads14/product/milk.jpg', 100, 1),
('限时秒杀 全场满减', '/uploads14/product/apple.jpg', 90, 1);
