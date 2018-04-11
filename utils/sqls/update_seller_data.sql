DELIMITER $$
CREATE PROCEDURE `update_seller_data`(IN in_seller_name VARCHAR(40), IN in_count INT, IN in_total_value DOUBLE)
BEGIN
	SELECT `number_of_sales`, `total_value` INTO @sale_count, @total_value FROM `sales` WHERE `seller_name` = in_seller_name;
    UPDATE `sales` SET `number_of_sales` = @sale_count + in_count, `total_value` = @total_value + in_total_value WHERE `seller_name` = in_seller_name;
END$$
DELIMITER ;