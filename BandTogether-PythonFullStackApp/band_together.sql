-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema band_together
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema band_together
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `band_together` DEFAULT CHARACTER SET utf8 ;
USE `band_together` ;

-- -----------------------------------------------------
-- Table `band_together`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `band_together`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `band_together`.`bands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `band_together`.`bands` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `founding_member` VARCHAR(255) NULL,
  `genre` VARCHAR(255) NULL,
  `home_city` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_bands_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_bands_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `band_together`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
