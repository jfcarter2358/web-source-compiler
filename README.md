# Web Source Compiler

# Usage

When first using the web-source-compiler in a project, run

```
wsc init
```

to generate a `.wsc` file.

After that, customize the file with the directories where your source files will be located (don't worry about ones that don't exist yet). Then, run

```
wsc setup
```

To create all missing directories for you.

When writing your code, you can create sub-modules for javascript, html, and css. Place them in the `modules` subdirectory with any main pages in the `main` subdirectory. You can then import the modules into any main file with the following comments:

## Javascript

```
// import <module name>
```

## html

```
<!-- import <module name> -->
```

## css

```
/* import <module name> -->
```

When you're ready to compile your code, run

```
wsc compileS
```