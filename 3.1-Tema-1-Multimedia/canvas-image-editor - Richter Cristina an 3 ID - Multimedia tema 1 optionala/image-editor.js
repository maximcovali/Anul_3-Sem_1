/* Assignment

8. Only display the download link when an effect is applied
8. (optional) Use Bootstrap for the UI (https://getbootstrap.com/)
9. (optional) Implement pixelate
Hint: check https://gist.github.com/anonymous/1888841
10. (optional)Check web workers as a way to perfrom heavy processing without blocking the UI thread
Hint: https://stackoverflow.com/questions/8170431/using-web-workers-for-drawing-using-native-canvas-functions
*/

'use strict';

let app = {
    originialImage: null,
    processedImage: null,
    donwloadLink: null,
    loader: null,
    currentEffect: null
}

//Drawing methods
app.changeEffect = function(effect){
    if(effect !== app.currentEffect)
    {
        app.currentEffect = effect;
        app.drawImage();
    }
}

app.drawImage = function() {
    
    //show spinner
    app.loader.style.display = 'block';

    //https://developer.mozilla.org/en-US/docs/Web/API/Performance/now
    let t0 = performance.now();
    console.log("t0: "+t0);

    let processingCanvas = document.createElement('canvas');
    processingCanvas.width = app.originialImage.naturalWidth;
    processingCanvas.height = app.originialImage.naturalHeight;
    let context = processingCanvas.getContext("2d");
    context.drawImage(app.originialImage, 0, 0, processingCanvas.width, processingCanvas.height);

    let t1 = performance.now();
    console.log(t1-t0 + ": drawing the image on the canvas");

    switch (app.currentEffect) {
        case "normal":
            app.normal(context);
            break;
        case "grayscale":
            app.grayscale(context);
            break;
        case "threshold":
            app.threshold(context);
            break;
        case "sephia":
            app.sephia(context);
            break;
        case "invert":
            app.invert(context);
            break;
        case "red":
            app.red(context);
            break;
        case "green":
            app.green(context);
            break;
        case "blue":
            app.blue(context);
            break;
    }

    let t2 = performance.now();
    console.log(t2-t1+": applying the effect on the canvas");
            
    processingCanvas.toBlob(function(blob){
        let blobUrl = URL.createObjectURL(blob);
        app.processedImage.src = blobUrl;
        app.donwloadLink.href = blobUrl;

        app.loader.style.display = 'none';

        let t3 = performance.now();
        console.log(t3-t2 + ": generating a blob from the processed canvas");
        
        console.log("finished");
    },"image/png");
}

app.normal = function(context){
    
}

app.grayscale = function(context){
    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    //let alternateWay = 0.2 * pixels[i] +  0.72 * pixels[i + 1] + 0.07 * pixels[i + 2];
    for (let i = 0; i < pixels.length; i+=4)
        //ORIGINAL VERSION
        pixels[i] = pixels[i + 1] = pixels[i + 2] = Math.round((pixels[i] + pixels[i + 1] + pixels[i + 2])/3);

        //ALTERNATE VERSION
        //pixels[i] = pixels[i+1] = pixels [i+2] = (0.2 * pixels[i] +  0.72 * pixels[i + 1] + 0.07 * pixels[i + 2]);
    context.putImageData(imageData, 0, 0); 
}

app.threshold = function(context){

/*
    1. Implement threshold
    Hint: v = (0.2126*r + 0.7152*g + 0.0722*b >= threshold) ? 255 : 0; r’= g’ = b’ = v
 */

    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+=4){
        let r = pixels[i];
        let g = pixels[i+1];
        let b = pixels[i+2];

        let v = 0.2126*r + 0.7152*g + 0.0722*b;

        if (v>127){
            pixels[i] = pixels[i+1] = pixels[i+2] = 255;
        }
        else pixels[i] = pixels[i+1] = pixels[i+2] = 0;
    }
    context.putImageData(imageData, 0, 0);     
}

app.sephia = function(context){

    /*
        2. Implement sephia
        Hint: 
        r' = (r * .393) + (g *.769) + (b * .189)
        g' = (r * .349) + (g *.686) + (b * .168)
        b' = (r * .272) + (g *.534) + (b * .131)
    */
    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+=4){
        pixels[i] = (pixels[i] * .393) + (pixels[i+1] * .769) + (pixels[i+2]*.189);
        pixels[i+1] = (pixels[i] * .349) + (pixels[i+1] * .686) + (pixels[i+2]*.168);
        pixels[i+2] = (pixels[i] * .272) + (pixels[i+1] * .534) + (pixels[i+2]*.131);
    }
    context.putImageData(imageData, 0, 0)
}

app.invert = function (context){

    /*
        3. Implement invert (negative)
        Hint: r' = 255 – r; g' = 255 – g; b' = 255 – b;
    */

    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+= 4){
        pixels[i] = 255 - pixels[i];        //red
        pixels[i+1] = 255 - pixels[i+1];    //green
        pixels[i+2] = 255 -pixels[i+2];     //blue
    }
    context.putImageData(imageData, 0, 0);
}

app.red = function(context){

    /*
        4. Implement red
        Hint: r'=r; g'=0; b'=0;
    */

    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+= 4){
        //pixels[i] = pixels[i];  //nu am inteles daca se doreste convertirea tuturor pixelilor la rosu 
        pixels[i] = 255;  //red
        pixels[i+1] = 0;        //green
        pixels[i+2] = 0;        //blue
    }
    context.putImageData(imageData, 0, 0);
}

app.green=function(context){

    /*
        5. Implement green
        Hint: r'=0; g'=255; b'=0;
    */
    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+= 4){
        pixels[i] = 0;          //red
        pixels[i+1] = 255;      //green
        pixels[i+2] = 0;        //blue
    }
    context.putImageData(imageData, 0, 0); 
}

app.blue=function(context){

    /*
        6. Implement blue
        Hint: r'=0; g'=0; b'=b;
    */

    let imageData = context.getImageData(0, 0, context.canvas.width, context.canvas.height);
    let pixels = imageData.data;
    for (let i = 0; i < pixels.length; i+= 4){
        pixels[i] = 0;          //red
        pixels[i+1] = 0;        //green
        pixels[i+2] = 255;      //blue
    }
    context.putImageData(imageData, 0, 0); 
}

//Events
app.load = function () {
    app.originialImage = document.createElement("img");
    app.donwloadLink = document.getElementById("donwloadLink");
    app.processedImage = document.getElementById("processedImage");
    app.loader = document.querySelector('.loader');
            
    app.originialImage.addEventListener("load",function(){
        app.currentEffect = null;
        app.changeEffect("normal");
    });

    app.originialImage.addEventListener('error', function (msg, source, lineNo) {
        alert("Mesaj eroare: {0}".format(msg));
    });

    let buttons = document.getElementsByClassName("effectType");
    for(let i=0; i<buttons.length; i++){
        //more about the data attribute: https://developer.mozilla.org/en/docs/Web/Guide/HTML/Using_data_attributes

        buttons[i].addEventListener("click", function(){ app.changeEffect(this.dataset.effect)}); 
    }

    document.getElementById("fileBrowser").addEventListener("change", function(e){  
        //1. create the reader
        let reader = new FileReader();
        //2. attach events
        reader.addEventListener('load', function(event){
            app.originialImage.src = event.target.result;
        });
        //3. start loading the file
        reader.readAsDataURL(e.target.files[0]);    
    });
}
