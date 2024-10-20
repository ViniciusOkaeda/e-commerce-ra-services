--create database e_commerce_db;
--use e_commerce_db;

create table users (
user_id INT auto_increment PRIMARY KEY NOT NULL,
username VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
name VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE
);

create table products_category (
products_category_id INT auto_increment PRIMARY KEY NOT NULL,
category_name VARCHAR(255) NOT NULL UNIQUE,
category_description VARCHAR(255) NOT NULL UNIQUE,
category_image VARCHAR(255) NOT NULL
);

create table sizes(
sizes_id INT auto_increment PRIMARY KEY NOT NULL,
sizes_name VARCHAR(10) NOT NULL UNIQUE
);

create table colors(
colors_id INT auto_increment PRIMARY KEY NOT NULL,
colors_name VARCHAR(50) NOT NULL UNIQUE
);

create table products (
products_id INT auto_increment PRIMARY KEY NOT NULL,
products_name VARCHAR(255) NOT NULL,
products_description VARCHAR(255) NOT NULL,
products_price float NOT NULL,
products_image VARCHAR(255) NOT NULL,
products_category_id INT NOT NULL,
foreign key(products_category_id) references products_category(products_category_id)
);

create table products_color(
products_color_id INT auto_increment PRIMARY KEY NOT NULL,
products_id INT NOT NULL,
colors_id INT NOT NULL,
foreign key (products_id) references products(products_id),
foreign key (colors_id) references colors(colors_id)
);

create table products_sizes (
products_sizes_id INT auto_increment PRIMARY KEY NOT NULL,
sizes_id INT NOT NULL,
products_id INT NOT NULL,
foreign key(sizes_id) references sizes(sizes_id),
foreign key(products_id) references products(products_id)
);

create table products_images (
products_images_id INT auto_increment PRIMARY KEY NOT NULL,
products_images VARCHAR(255) NOT NULL,
products_id INT NOT NULL,
foreign key(products_id) references products(products_id)
);

create table favorites (
favorites_id INT auto_increment PRIMARY KEY NOT NULL,
user_id INT NOT NULL,
products_id INT NOT NULL,
foreign key(user_id) references users(user_id),
foreign key(products_id) references products(products_id)
);

CREATE TABLE favorite_product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(products_id) ON DELETE CASCADE
);

