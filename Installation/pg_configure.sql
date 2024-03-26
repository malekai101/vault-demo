CREATE TABLE public.tb_football_teams (
    city       varchar(40) NOT NULL,
    team_name        varchar(10) NOT NULL
);
INSERT INTO tb_football_teams (city, team_name) VALUES ('New York', 'Jets');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Buffalo', 'Bills');
INSERT INTO tb_football_teams (city, team_name) VALUES ('New England', 'Patriots');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Miami', 'Dolphins');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Tennessee', 'Titans');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Houston', 'Texans');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Indianapolis', 'Colts');
INSERT INTO tb_football_teams (city, team_name) VALUES ('Jacksonville', 'Jaguars');

CREATE ROLE "ro" NOINHERIT;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "ro";
