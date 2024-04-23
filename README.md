<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        #head {
            background-color: black;
            color: white;
            padding: 10px;
            text-align: center;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 15px;
            font-weight: bold;
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            margin-top: 20px;
            margin-left: 20px;
            margin-right: 20px;
            transition: 0.5s;
            cursor: pointer;
            position: relative;
        }
        #head:hover {
            box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.5);
            transform: scale(1.03);
        }
        #head:active {
            box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.5);
            transform: scale(0.9);
        }
        #about {
            color: rgb(255, 255, 255);
            padding: 10px;
            text-align: left;
            font-family: Arial, Helvetica, sans-serif;
}
        #content-table {
            margin-top: 20px;
            margin-left: 20px;
            margin-right: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
        }
        #about-icon {
            image-resolution:calc(
                var(--image-resolution, 100%) / 100%
            );
            text-align: center;
            align-items: center;
            display: flex;
            justify-content: space-between;
        }
        i {
            padding: 10px;
        }
        a {
            text-decoration: none;
            color: white;
        }
        a:hover {
            color: rgb(174, 171, 171);
            text-decoration: none;
            font-weight: bold;
        }
</style>
</head>
<body>
    <div id="head"> 
        <h1>Wellcome to scrape API</h1>
        <br>
        <hr>
        <div id="content-table">
            <div id="about-icon">
                <i><img width="30" height="30" src="https://img.icons8.com/pastel-glyph/30/FFFFFF/info--v3.png" alt="info--v3"/></i>
                <a href="#about">About</a>
            </div>
            <div id="about-icon">
                <i><img width="30" height="30" src="https://img.icons8.com/external-sbts2018-solid-sbts2018/30/FFFFFF/external-install-basic-ui-elements-2.3-sbts2018-solid-sbts2018.png" alt="external-install-basic-ui-elements-2.3-sbts2018-solid-sbts2018"/></i>
                <a href="#install">install</a>
            </div>
            <div id="about-icon">
                <i><img width="30" height="30" src="https://img.icons8.com/ios/30/FFFFFF/trial-version.png" alt="trial-version"/></i>
                <a href="#demonstration">demonstration</a>
            </div>
            <div id="about-icon">
                <i><img width="30" height="30" src="https://img.icons8.com/external-others-nixx-design/30/FFFFFF/external-documentation-web-design-lineal-others-nixx-design.png" alt="external-documentation-web-design-lineal-others-nixx-design"/></i>
                <a href="#documentation">documentation</a>
            </div>

</div>
    </div>
    <div id="about">
        <h1>About</h1>
        <p>This is a simple API for scraping data from Wikipedia</p>
    </div>
</body>
</html>