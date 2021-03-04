CREATE TABLE `user` (
  `id` INTEGER PRIMARY KEY,
  `name` TEXT NOT NULL,
  `money` REAL DEFAULT 0
);

CREATE TABLE `order_status` (
  `code` TEXT PRIMARY KEY,
  `name` TEXT
);
INSERT INTO `order_status` VALUES ('OPEN', 'Open');
INSERT INTO `order_status` VALUES ('COMP', 'Complete');
INSERT INTO `order_status` VALUES ('CANC', 'Cancelled');

CREATE TABLE `order_type` (
  `code` TEXT PRIMARY KEY,
  `name` TEXT
);
INSERT INTO `order_status` VALUES ('BUY', 'Buy');
INSERT INTO `order_status` VALUES ('SELL', 'Sell');

CREATE TABLE `order` (
  `id` INTEGER PRIMARY KEY,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `type` TEXT NOT NULL,
  `user` INTEGER NOT NULL,
  `status` TEXT DEFAULT 'OPEN',
  `quantity` INTEGER NOT NULL,
  `price` REAL NOT NULL,
  
  FOREIGN KEY (`type`) REFERENCES `order_type` (`code`),
  FOREIGN KEY (`status`) REFERENCES `order_status` (`code`),
  FOREIGN KEY (`user`) REFERENCES `user` (`id`)
);

CREATE TABLE `interaction_status` (
  `code` TEXT PRIMARY KEY,
  `name` TEXT
);
INSERT INTO `order_status` VALUES ('PEND', 'Pending');
INSERT INTO `order_status` VALUES ('APPR', 'Approved');

CREATE TABLE `interaction` (
  `id` INTEGER PRIMARY KEY,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user` INTEGER NOT NULL,
  `order` INTEGER NOT NULL,
  `quantity` INTEGER NOT NULL,
  `status` INTEGER DEFAULT 'PEND',

  FOREIGN KEY (`order`) REFERENCES `order` (`id`),
  FOREIGN KEY (`status`) REFERENCES `interaction_status` (`code`),
  FOREIGN KEY (`user`) REFERENCES `user` (`id`)
);
