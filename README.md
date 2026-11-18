# Webapp developing: practice 1

Field: Race Championships

Entities: Drivers, Races

## Run


```shell
docker-compose up
```
```shell
uvicorn app.main:app --reload
```

## DB

```shell
docker exec -t webapp-lab-db pg_dump -U admin -d postgres -f /tmp/dump.sql
docker cp webapp-lab-db:/tmp/dump.sql ./dump.sql
```
```shell
docker cp ./dump.sql webapp-lab-db:/tmp/dump.sql
docker exec -it webapp-lab-db psql -U admin -d postgres -f /tmp/dump.sql
 ```


## Test data

### Drivers

```json
[
  {
    "name": "Max Verstappen",
    "country": "NL",
    "team": "Red Bull Racing",
    "number": 3
  },
  {
    "name": "Lando Norris",
    "country": "GB",
    "team": "McLaren",
    "number": 1
  },
  {
    "name": "Charles Leclerc",
    "country": "MC",
    "team": "Ferrari",
    "number": 16
  }
]
```

### Races

```json
[
  {
    "championship": "Formula 1",
    "name": "Italian Grand Prix",
    "start_date": "2026-09-06T15:00:00",
    "time": "2:00:00",
    "track": "Autodromo Nazionale Monza"
  },
  {
    "championship": "FIA World Endurance Championship",
    "name": "24 Hours of Le Mans",
    "start_date": "2026-06-13T16:00:00",
    "time": "24:00:00",
    "track": "Circuit de la Sarthe"
  }
]
```

## SQL

### Clear
```postgresql
TRUNCATE TABLE drivers_in_races, drivers, races RESTART IDENTITY CASCADE;
```
### Fill

```postgresql
-- 1. Додаємо гонщиків (Formula 1, WEC, WRC, MotoGP)
INSERT INTO drivers (name, country, team, number, rating) VALUES
-- Formula 1
('Lewis Hamilton', 'GB', 'Scuderia Ferrari', 44, 96),
('Max Verstappen', 'NL', 'Red Bull Racing', 1, 98),
('Lando Norris', 'GB', 'McLaren Formula 1 Team', 4, 94),
('Fernando Alonso', 'ES', 'Aston Martin Aramco', 14, 93),
('Carlos Sainz', 'ES', 'Williams Racing', 55, 91),
('Oscar Piastri', 'AU', 'McLaren Formula 1 Team', 81, 92),

-- WEC (24 Hours of Le Mans)
('Antonio Fuoco', 'IT', 'Ferrari AF Corse', 50, 90),
('Kamui Kobayashi', 'JP', 'Toyota Gazoo Racing', 7, 91),
('Kevin Estre', 'FR', 'Porsche Penske Motorsport', 6, 92),

-- WRC (Ралі)
('Sebastien Ogier', 'FR', 'Toyota Gazoo Racing WRT', 17, 97),
('Thierry Neuville', 'BE', 'Hyundai Shell Mobis WRT', 11, 94),
('Kalle Rovanpera', 'FI', 'Toyota Gazoo Racing WRT', 69, 95),

-- MotoGP
('Valentino Rossi', 'IT', 'Team WRT (GT3 / Legend)', 46, 99),
('Marc Marquez', 'ES', 'Ducati Lenovo Team', 93, 97),
('Francesco Bagnaia', 'IT', 'Ducati Lenovo Team', 1, 95);


-- 2. Додаємо перегони
INSERT INTO races (name, championship, start_date, duration, track) VALUES
('Monaco Grand Prix', 'Formula 1', '2026-05-24 15:00:00+02', '2 hours', 'Circuit de Monaco'),
('Silverstone Grand Prix', 'Formula 1', '2026-07-05 15:00:00+01', '2 hours', 'Silverstone Circuit'),
('Suzuka 8 Hours', 'FIM Endurance World Championship', '2026-07-19 11:30:00+09', '8 hours', 'Suzuka International Racing Course'),
('24 Hours of Spa', 'GT World Challenge Europe', '2026-06-27 16:30:00+02', '24 hours', 'Circuit de Spa-Francorchamps'),
('Rallye Monte-Carlo', 'WRC', '2026-01-22 18:00:00+01', '4 days', 'Col de Turini'),
('Italian Motorcycle Grand Prix', 'MotoGP', '2026-05-31 14:00:00+02', '45 minutes', 'Autodromo Internazionale del Mugello');


-- 3. Зв'язуємо гонщиків із гонками (через підзапити, щоб не гадати з ID)
INSERT INTO drivers_in_races (driver_id, race_id)
SELECT d.id, r.id
FROM drivers d
JOIN races r ON
    -- Учасники F1 на етапах в Монако та Сільверстоуні
    (d.name IN ('Lewis Hamilton', 'Max Verstappen', 'Lando Norris', 'Fernando Alonso', 'Carlos Sainz', 'Oscar Piastri')
     AND r.name IN ('Monaco Grand Prix', 'Silverstone Grand Prix'))
    OR
    -- Пілоти WEC + легендарний Россі на марафоні 24 години Спа
    (d.name IN ('Antonio Fuoco', 'Kamui Kobayashi', 'Kevin Estre', 'Valentino Rossi')
     AND r.name = '24 Hours of Spa')
    OR
    -- Ралійники на Ралі Монте-Карло
    (d.name IN ('Sebastien Ogier', 'Thierry Neuville', 'Kalle Rovanpera')
     AND r.name = 'Rallye Monte-Carlo')
    OR
    -- Мотогонщики на етапі в Муджелло
    (d.name IN ('Marc Marquez', 'Francesco Bagnaia', 'Valentino Rossi')
     AND r.name = 'Italian Motorcycle Grand Prix')
    OR
    -- Кобаяші та Маркес на гонці в Сузуці
    (d.name IN ('Kamui Kobayashi', 'Marc Marquez')
     AND r.name = 'Suzuka 8 Hours');
```