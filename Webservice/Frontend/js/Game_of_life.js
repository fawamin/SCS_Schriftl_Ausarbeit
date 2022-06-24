

function buildField()
{
    //Canvas and context object
    var canvas = document.getElementById("GOLCanvas");
    var ctx = canvas.getContext("2d");
    //Variables for width and height of Canvas
    var width = canvas.width;
    var height = canvas.height;
    // Fill canvas with white
    ctx.fillStyle = "#FFFFFF"; 
    let answer = fetch(`http://localhost:8000/gol`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ Filename: "5x5test" })})
    .then(response =>{
        fetch("http://localhost:8000/gol",{method: 'GET'})
        .then(response => response.json())
        .then(data => 
            data.forEach(
                element => {
                    console.log(element);
                     }
                )
            );
    });
    //row * width - 2 ,col * height -2 , width -2 , height- 2
}

function set_file()
{

}
