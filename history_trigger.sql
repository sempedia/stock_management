DELIMITER //
DROP TRIGGER IF EXISTS after_stock_mng_stock_update//
CREATE TRIGGER after_stock_mng_stock_update AFTER UPDATE ON stock_mng_stock FOR EACH ROW
BEGIN  
	IF new.issued_quantity = 0
		THEN INSERT INTO stock_mng_stockhistory(
			id,
			last_updated,
			category_id,
			item_name,
            issued_quantity,
			quantity,
			received_quantity,
			received_by)
		VALUES(
			new.id,
			new.last_updated,
			new.category_id,
			new.item_name,
            new.issued_quantity,
			new.quantity,
			new.received_quantity,
			new.received_by);
	ELSEIF new.received_quantity = 0
		THEN INSERT INTO stock_mng_stockhistory(
			id,
			last_updated,
			category_id,
			item_name,
            received_quantity,
			quantity,
			issued_quantity,
			issued_by,
            issued_to)
		VALUES(
			new.id,
			new.last_updated,
			new.category_id,
			new.item_name,
            new.received_quantity,
			new.quantity,
			new.issued_quantity,
			new.issued_by,
            new.issued_to);
	END IF;
END//
DELIMITER ;
    
