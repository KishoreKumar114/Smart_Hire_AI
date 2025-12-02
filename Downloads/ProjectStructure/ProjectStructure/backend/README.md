### Starter Backend

<br>
Required softwares:

1. Docker Desktop
2. Nest CLI (npm i -g @nestjs/cli)
3. All plugins recommended in VS Code for this project

To start development process, run:

`npm run dev:start`

To stop development process, run:

`npm run dev:stop`

Every time a new package is installed, run:

`npm run dev:restart`

Generate a new migration, run:

`npm run migration:generate:dev src/shared/database/migration/{Migration Name}`

Apply a migration, run:

`npm run migration:run:dev`
