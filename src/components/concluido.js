const template = document.createElement('template');
template.innerHTML = `
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        div{
            border:solid 5px #A8A7A7;
            border-radius: 20px;
            background-color: #fcfcfc;
            width: 1010px;
            height: 250px;
            font-family:'Poppins', sans-serif;
            display : flex;
            align-items : center;
            flex-direction: column;
        }

        p{
            padding: 30px 0px 20px 0px; 
            font-size: 36px;
        }


        button{
            border:none;
            font-size:24px;
            color:rgba(0, 0, 0, 1);
            background-color: rgba(87, 218, 116, 0.7);
            border-radius:10px;
            height: 60px;
            width: 300px;
            margin:40px 0px 56px 0px;
        }
    </style>
    
    <div>
        <p>Critério de Rejeição</p>  
        <button>Concluído</button>
    </div>
       
`;

class Concluir extends HTMLElement{
    constructor(){
        super();
        console.log('criado');

        this.attachShadow( {mode:'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

    }

    connectedCallback(){
        console.log('callback');
        const button = this.shadowRoot.querySelector('button');
        
    }
}

window.customElements.define('conclu-ir', Concluir);