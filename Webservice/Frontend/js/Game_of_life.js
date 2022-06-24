

function buildField()
{
    //Canvas and context object
    var canvas = document.getElementById("GOLCanvas");
    var ctx = canvas.getContext("2d");
    //Variables for width and height of Canvas
    var Canvaswidth = canvas.width;
    var Canvasheight = canvas.height;
    // Fill canvas with white
    ctx.fillStyle = "#000000"; 
    let answer = fetch(`http://localhost:8000/gol`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ Filename: "5x5test" })})
    .then(response =>{
        fetch("http://localhost:8000/gol",{method: 'GET'})
        .then(response => response.json())
        .then(data => {
            let width = Canvaswidth / data.length
            let height = Canvasheight / data.length
            for(let row = 0; row< data.length; row++)
            {
                for(let col = 0; col < data[row].length; col++)
                {
                    if(data[row][col] == 0)
                    {
                        ctx.fillStyle = "#FFFFFF"; 
                    }
                    else
                    {
                        ctx.fillStyle = "#000000"; 
                    }
                    ctx.fillRect(row * width - 2 ,col * height -2 , width -2 , height- 2)
                }
            }
        });
    });
    //row * width - 2 ,col * height -2 , width -2 , height- 2
}

function set_file()
{

}
