const template = document.createElement('template');
template.innerHTML = `  
    <style type="text/css">
        * {
            padding: 0;
            margin: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        .legenda {
            display: flex;
            align-items: center;
            justify-content:space-evenly;
        }

        .hardware, .software, .info{
            border: solid 2px #A8A7A7;
            border-radius: 10px;
            height: 70px;
            width: 350px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 16px;
        }

        .categoria{
            font-weight: 600;
            font-size: 18px;
        }

        .quant{
            font-size: 12px;
            font-weight: 400;
        }

        .icon{
            width: 50px;
            height: 50px;
        }
        </style>

        <div class="legenda">
            <div class="hardware">
                <div>
                    <p class="categoria">Problemas de Hardware</p>
                    <p class="quant">Quantidade:???</p> <!--variavel de quantidade-->
                </div>    
            <img class="icon" src="../static/images/Hardware.png" alt="hardware">
        </div>   

            <div class="software">
                <div>
                    <p class="categoria">Problemas de Software</p>
                    <p class="quant">Quantidade:???</p> <!--variavel de quantidade-->
                </div>    
                <img class="icon" src="../static/images/Software.png" alt="hardware">
            </div>  

            <div class="info">
                <div>
                    <p class="categoria">Esclarecimento/informação</p>
                    <p class="quant">Quantidade:???</p> <!--variavel de quantidade-->
                </div>    
                <img class="icon" src="../static/images/Info.png" alt="hardware">
            </div>  
        </div>   
`;
    
class cardlegenda extends HTMLElement {
    constructor(){
        super();

        this.attachShadow({mode:'open'})
        this.shadowRoot.appendChild(template.content.cloneNode(true))
    }  
}

window.customElements.define('card-legenda', cardlegenda);