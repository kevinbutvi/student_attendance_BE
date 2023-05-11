-- CREATE TABLE SUBJECTS
CREATE TABLE `attendanceAPP`.`Subjects` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id`));


-- CREATE TABLE STUDENTS
CREATE TABLE `attendanceAPP`.`Students` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    `lastName` VARCHAR(45) NOT NULL,
    `dni` BIGINT(45) NOT NULL,
    PRIMARY KEY (`id`));

CREATE TABLE `attendanceAPP`.`Student_Subject` (
    `studentId` INT NOT NULL,
    `subjectId` INT NOT NULL,
    PRIMARY KEY (`studentId`, `subjectId`),
    INDEX `student_subjecto_to_subject_idx` (`subjectId` ASC) VISIBLE,
    CONSTRAINT `student_subject_to_student`
        FOREIGN KEY (`studentId`)
        REFERENCES `attendanceAPP`.`Students` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `student_subjecto_to_subject`
        FOREIGN KEY (`subjectId`)
        REFERENCES `attendanceAPP`.`Subjects` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE);

-- CREATE TABLE CLASSES
CREATE TABLE `attendanceAPP`.`Classes` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `subjectId` INT NOT NULL,
    `duration` TIME NOT NULL,
    `date` DATE NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `classes_to_subject_idx` (`subjectId` ASC) VISIBLE,
    CONSTRAINT `classes_to_subject`
        FOREIGN KEY (`subjectId`)
        REFERENCES `attendanceAPP`.`Subjects` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE);



-- INSERT EXAMPLE DATA

-- SUBJECT
INSERT INTO attendanceAPP.Subjects (name) VALUE ("Python");

-- STUDENTS
INSERT INTO attendanceAPP.Students (name, lastName, dni) 
VALUES 
    ("Jhon", "Doe", 44333222), 
    ("Isabella", "Martinez", 1444777),
    ("Emma", "Johnson", 77888999),
    ("Alex", "Kim", 33222111),
    ("Olivia", "Rodriguez", 99887766),
    ("William", "Thompson", 55443322),
    ("Sophia", "Garcia", 77665544),
    ("Ethan", "Hernandez", 22113344);

-- STUDENTS INTO CALSS
INSERT INTO attendanceAPP.Student_Subject (subjectId, studentId) 
VALUES 
    (1,1),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (1,6),
    (1,7),
    (1,8);

-- CLASSES
INSERT INTO attendanceAPP.Classes (subjectId, duration, date) 
VALUES 
    (1, "01:05:45", "2023-04-25"),
    (1, "01:15:22", "2023-04-26"),
    (1, "02:12:09", "2023-04-27"),
    (1, "01:38:56", "2023-04-28"),
    (1, "00:50:33", "2023-04-29"),
    (1, "01:17:19", "2023-04-30"),
    (1, "02:19:01", "2023-05-01"),
    (1, "01:44:27", "2023-05-02");
