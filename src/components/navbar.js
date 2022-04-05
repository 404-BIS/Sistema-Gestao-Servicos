const template = document.createElement('template');
template.innerHTML = `
    <style>
        *{
            margin:0;
            padding:0;
            box-sizing: border-box;
        }

        header {
            display:flex;
            align-items:center;
            justify-content: space-between;
            background-color:#B8D7D9;
            padding: 5px 170px;
            font
        }

        nav {
            display:flex;
            justify-contentent:space-beetwen;
            align-items:center;
            font-family: 'Poppins', sans-serif;
        }

        p {
            font-size: 18px; 
            color:#6D6D6D; 
            background-color:#B8D7D9; 
            border:none;
            margin-right:60px

        }

        button {
            font-size: 18px; 
            color:#6D6D6D; 
            background-color:#FCFCFC; 
            border:none;
            border-radius: 8px;
            width:200px;
            Height:30px;
        }
        
    </style>
    
        <header>
            <img src="user.png"> 
            <nav>
                <p class="minhareq">Minhas requisições</p>
                <button name="novareq">Nova Requisição</button>
            </nav>
        </header>
    
`;

class Navbar extends HTMLElement{
    constructor(){
        super();
        console.log('criado');

        this.attachShadow( {mode:'open'});
        this.shadowRoot.appendChild(template.content.cloneNode(true));

    }

    connectedCallback(){
        console.log('callback');
        const nav = this.shadowRoot.querySelector('nav');
        
    }
}

window.customElements.define('nav-bar', Navbar);