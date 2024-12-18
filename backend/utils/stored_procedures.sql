DROP PROCEDURE IF EXISTS get_image_length;
--#--new--#
CREATE PROCEDURE get_image_length(IN id INT, OUT result INT)
Begin
	SELECT LENGTH(image) FROM demons
	WHERE ID=id;
END;
--#--new--#
DROP PROCEDURE IF EXISTS get_chonked_image;
--#--new--#
CREATE PROCEDURE get_chonked_image(IN id INT, IN start_index INT, in end_index INT, OUT result INT)
Begin
	SELECT SUBSTRING(image,start_index,end_index) FROM demons
	where ID=id;
END;
