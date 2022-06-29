window.addEventListener("DOMContentLoaded",()=>{
    document.getElementById("newDay").addEventListener("click",() => {
        fetch(`http://localhost:8000/gol/cycle`, {method: 'POST'})
        buildField()
    });
});
function firstload()
{
    fetch(`http://localhost:8000/gol`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ Filename: "10x10Glider" })})
    .then(response =>{
        buildField();
    })
}

function buildField()
{
    //Canvas and context object
    var canvas = document.getElementById("GOLCanvas");
    var ctx = canvas.getContext("2d");
    //Variables for width and height of Canvas
    var Canvaswidth = canvas.width;
    var Canvasheight = canvas.height;
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
                ctx.fillRect( (row * width) -2  , (col * height) -2 , width -2 , height- 2)
            }
        }
    });
    //row * width - 2 ,col * height -2 , width -2 , height- 2
}

function set_file()
{

}
