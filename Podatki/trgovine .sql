CREATE TABLE IF NOT EXISTS trgovine (
    `id_trgovine` INT,
    `ime_trgovine` VARCHAR(8) CHARACTER SET utf8,
    `lokacija` VARCHAR(24) CHARACTER SET utf8
);
INSERT INTO trgovine VALUES
    (1,'spar','Corfe Alley'),
    (2,'spar','Highlands Cliff'),
    (3,'spar','Broad Heights'),
    (4,'spar','Gibson Loke'),
    (5,'spar','Ellicks Close'),
    (6,'mercator','Hornhatch'),
    (7,'mercator','Laburnum Lane'),
    (8,'mercator','Thorpe Leys'),
    (9,'mercator','Waterside Boulevard'),
    (10,'mercator','Millbrook Market'),
    (11,'tus',' Beeches Oak'),
    (12,'tus','Priory Crescent'),
    (13,'hofer','Cromer Point'),
    (14,'hofer','Dingle Close'),
    (15,'hofer','Rydal Square'),
    (16,'hofer','Beechcroft Wynd'),
    (17,'lidl','Mount Pleasant Woodlands'),
    (18,'lidl','Priors Bridge'),
    (19,'lidl','Bull Isaf'),
    (20,'lidl','Bernard Fairway');
