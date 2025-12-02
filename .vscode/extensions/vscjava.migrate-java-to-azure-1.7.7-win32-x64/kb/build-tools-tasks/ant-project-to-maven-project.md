---
id: ant-project-to-maven-project
title: Ant Project to Maven Project
description: Migrate Ant project to Maven project
hierarchy: Build Tool Tasks
---

# Migrate Ant project to Maven project

## Success measurement

 - No source code changed, only build files and directory structure changed.

## Caution points about commands
1. Use `mv` command instead of `cp` to avoid duplicated files.
2. Don't move a parent folder's contents directly into its child folder because it will cause infinite loop. Use this method instead: rename the folder then move its contents. For example: Use `mv src src_temp && mkdir -p src/main/java && mv src_temp/* src/main/java/` instead of `mv src/* src/main/java/`.
3. Don't use a backslash before double quotation marks (or as the last character) in your command, as backslash is an escape character. For example: `cp -r "src\ca" "src_temp\"` will cause the terminal to block waiting for additional input.

## Migration steps

Follow these steps to migrate an Ant project to a Maven project:

### Step 1: Create Maven build file from existing Ant build file

Create pom.xml based on files like build.xml

### Step 2: Handle jar files

Handle all jar files (**/*.jar) in the project by these steps one by one:
1. List all jar files in the current project to a new file in project root directory named `jar-files.md`. Example:
   ```md
   - [ ] file-one.jar
   - [ ] file-two.jar
   ```
2. Update `jar-files.md` indicating whether each jar can be downloaded from Maven central repository. Example of updated `jar-files.md`:
    ```md
    - [x] file-one.jar. Exists in Maven central repository
    - [x] file-two.jar. Does not exist in Maven central repository
3. Add the jar file into the `dependencies` section in `pom.xml`
   - If it exists in Maven central repository, add it into `pom.xml` directly.
   - If it doesn't exist in Maven central repository, use `system` scope in pom.xml for them. Example:
        ```xml
        <dependency>
            <groupId>custom.library</groupId>
            <artifactId>custom-name</artifactId>
            <version>1.0</version>
            <scope>system</scope>
            <systemPath>${project.basedir}/lib/custom-library.jar</systemPath>
        </dependency>
        ```
4. Delete all jar files that exist in Maven central repository.

### Step 3: Modify directory structure to fit Maven's convention

Refer to `Caution points about commands` section when modifying structure.

### Step 4: Clean up
1. Update `.gitignore` file, for example: `**/target/` should be included. But don't ignore the jar files that are used as `system` scope dependencies.
2. Delete Ant build files like `build.xml`.
3. Delete any duplicated files caused by `cp` command if there are such files.
