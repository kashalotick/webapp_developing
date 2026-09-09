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
    "country": "Netherlands",
    "team": "Red Bull Racing",
    "number": 3
  },
  {
    "name": "Lando Norris",
    "country": "United Kingdom",
    "team": "McLaren",
    "number": 1
  },
  {
    "name": "Charles Leclerc",
    "country": "Monaco",
    "team": "Ferrari",
    "number": 16
  },
  {
    "name": "Lewis Hamilton",
    "country": "United Kingdom",
    "team": "Ferrari",
    "number": 44
  },
  {
    "name": "Nyck de Vries",
    "country": "Netherlands",
    "team": "Toyota Gazoo Racing",
    "number": 7
  },
  {
    "name": "Kamui Kobayashi",
    "country": "Japan",
    "team": "Toyota Gazoo Racing",
    "number": 7
  },
  {
    "name": "Sébastien Buemi",
    "country": "Switzerland",
    "team": "Toyota Gazoo Racing",
    "number": 8
  },
  {
    "name": "Brendon Hartley",
    "country": "New Zealand",
    "team": "Toyota Gazoo Racing",
    "number": 8
  },
  {
    "name": "Alex Lynn",
    "country": "United Kingdom",
    "team": "Cadillac Hertz Team JOTA",
    "number": 12
  },
  {
    "name": "Will Stevens",
    "country": "United Kingdom",
    "team": "Cadillac Hertz Team JOTA",
    "number": 12
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
  },
  {
    "championship": "GT World Challenge Europe",
    "name": "24 Hours of Spa",
    "start_date": "2026-06-27T16:30:00",
    "time": "24:00:00",
    "track": "Circuit de Spa-Francorchamps"
  }
]
```