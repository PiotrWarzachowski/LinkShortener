# LinkShortener

LinkShortener is a Python made program that creates custom links with stats automatically and semi-automatically. It let's you see all the statistics in NoSQL databse.

## Run source code manually

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements.

```bash
pip install -r requirements.txt
```

run main.py using ***Python **3.X.X***** compiler.


## Usage
There are 4 endpoints:
* GET */* - The basic Endpoint that returns Text 
* POST */shorten* - Allows you to shorten any link in according format
   For random link generation ```{"url" : "link to redirect", "custom" : ""}```  
   For fixed link generation ```{"url" : "link to redirect", "custom" : "customphrase"}```  
* GET */get_views/customcode* - Allows you to get views for each custom link you have created
* GET */customcode* - Redirects to a url you provided
## Working Build

Working build (exe file) will be added once the project has more utility.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
