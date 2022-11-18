# std_doc
Utility for automatically creating the framework for documenting python modules

## Usage
This was written to be used with PyCharm, but the script is freestanding, and can either be applied to a file with the command line, or (probably) be added to other IDEs

### Adding to PyCharm
1. Download the executable zip and unpack it somewhere you can find it (and intend to keep it!)
2. In PyCharm go to File>Settings>Tools>File Watchers
3. Create a new file watcher:
![image](https://user-images.githubusercontent.com/101142254/202812692-e22ee893-b5d1-46ce-b4ff-8dd1217b23b1.png)
4. Adjust the settings like this:
![image](https://user-images.githubusercontent.com/101142254/202813286-c17ac92a-e668-4a95-bc61-acb70edae93c.png)

NOTE: You might want to change the scope to ignore test files, __init__.py files, and your error handler

5. Save your file watcher and give it a go

### Running From CMD - with just the .exe
Note: I have not tested this with anything other than windows, sorry.
This one's nice and easy :) just run the following command:

```
docstring_writer.exe -f "[path to project repo]\tests\test_files\test_input.py"
```

### Running from CMD - using the project files
If you want to fiddle with the way the docs get written, clone this repository, make your changes ([probably mostly to this file](..blob/master/std_doc/docstring_writer.py)), and you can run directly from the .py file as follows:
```
python "[path to project repo]\std_doc\docstring_writer.py" -f [filepath of .py file to document]
```
If you want to create an .exe from your file, just run the following commands (I added them to a .bat file while testing to make my life easier):
```
cd [path to project repo]
python std_doc\setup.py install
python std_doc\setup.py py2exe
cd dist
docstring_writer.exe -f "[path to project repo]\tests\test_files\test_input.py"
cd ..
```

## What Do The Results Look Like?
So... when you run it for the first time, it's gonna throw up a whole bunch of TODOs, to show you where everything should go:
![image](https://user-images.githubusercontent.com/101142254/202816368-a0f045ed-1c61-4f1b-b7dc-0c085a439e03.png)

(This is from the [desired output for the tests](..blob/master/tests/test_files/correct_output.py)
You'll see here that any existing documentation you've written will be preserved, either under its heading, if you've given it one, or under TEMP NOTES. If you give it a proper heading, it will always be preserved, and it won't raise TODOs

Anyway, once you've done all of the documentation, this is what the PyCharm documentation window will look like ([from docstring_writer.py](..blob/master/std_doc/docstring_writer.py)):
### Module Docstring
![image](https://user-images.githubusercontent.com/101142254/202815675-644bbb40-f63f-4389-84ff-8b4e025ff0a1.png)

### Class Docstring
![image](https://user-images.githubusercontent.com/101142254/202815895-4262f403-9c86-4929-8fa8-41f8caa7b5de.png)

### Function Docstring
![image](https://user-images.githubusercontent.com/101142254/202816140-640f205d-e46f-448c-9753-efd73612c187.png)


## Road Map
TODO:
1. Highlight properties
2. Add functionality to hide private functions
3. Change the documentation for properties too - its unnecesary to have the purpose and the ':returns:' for properties


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License. See `LICENSE` for more information.
