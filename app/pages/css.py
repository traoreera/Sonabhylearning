from .import *


class IDENTIC:
    BUTTON_STYLE = """
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        width: 100%;
        padding: 10px;
        background-color: #4CAF50;
        border: none;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        cursor: pointer;
    """

    CARDS_DYNAMIC: str = """
        :root {
            color-scheme: light dark; /* Prend en charge les thèmes */
        }
        .grid-container {
            display: grid;            
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));            
            gap: 1rem;            
            padding: 1rem;
        }      
        .card {            
            padding: 1rem;            
            border-radius: var(--pico-border-radius);            
            box-shadow: var(--pico-shadow);
        }        
        .icon {            
            font-size: 2rem;        
        }              
        .badge {
            background-color: var(--pico-primary);
            color: var(--pico-primary-inverse);
            padding: 0.3rem 0.7rem;
            border-radius: var(--pico-border-radius);        
        }
        .text2 {            
            font-size: 0.9rem;            
            color: var(--pico-muted-color);        
        }
    """

    BLUE_EFFET: str = """
        background-color: rgba(0,0,0,0.1);
        border-radius: 5px;
        box-shadow: -1px 0px 30px 17px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(6.5px);
        -webkit-backdrop-filter: blur(6.5px);
        border: 1px solid rgb(125 106 106 / 0%);
    """

    def __init__(self):
        super().__init__()
        return


class LOGIN(IDENTIC):

    DIV_STYLE: str = """
        height: 90vh;
        display: flex;
        align-items: center;
        justify-content: center;
    """
    FORM_STYLE: str = """
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 400px;
        width: 90%;
    """

    def __init__(self):
        super().__init__()
        return


class REGISTER(IDENTIC):
    H2_STYLE = """
        margin-bottom: 20px;
        text-align: center;
    """

    BODY_STYLE: str = """
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh;
        margin: 0;
        """

    CONTAINER_STYLE: str = """
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        width: 300px;
        """

    LABEL_STYLE: str = """
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    """

    INPUT_STYLE: str = """
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
    """

    def __init__(self):

        super().__init__()
        return


class HOMECSS(IDENTIC):
    
    CSS:str = """
            *{
                padding: 0;
                margin: 0;
                box-sizing: border-box;
                font-family: 'poppins',sans-serif;
            }

            .user{
                position: relative;
                width: 50px;
                height: 50px;
            }
            .user img{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;

            }
            .topbar{
                position: fixed;
                background: #fff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.08);
                width: 100%;
                height: 60px;
                padding: 0 20px;
                display: grid;
                grid-template-columns: 2fr 10fr 0.4fr 1fr;
                align-items: center;
                z-index: 1;
            }
            .logo{
                color: #299863;
            }
            .search{
                position: relative;
                width: 60%;
                justify-self: center;
            }
            .search input{
                width: 100%;
                height: 40px;
                padding: 0 40px;
                font-size: 16px;
                outline: none;
                border: none;
                border-radius: 10px;
                background: #f5F5F5;
            }
            .search i{
                position: absolute;
                right: 15px;
                top: 15px;
                cursor: pointer;
            }


            /* affichage du main */
            .main{
                position: absolute;
                top: 60px;
                background: #f5F5F5;
                width: 100%;
                height: 90%;
            }
            .cards{
                width: 100%;
                padding: 15px 20px;
                display: grid;
                grid-template-columns: repeat(4,1fr);
                grid-gap: 20px;
            }
            .cards .card{
                padding: 20px;
                padding-top: 10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 7px 25px 0 rgba(0,0,0,0.08);
                transition: 0.5s;
            }
            .cards .card:hover{
                background: #e8ebe9;
                transform: translateY(-18px);

            }
            .cards .card:hover .number{
                color: #fff;
            }
            .card-container{
                width: 100%;
            }

            .cards .card:hover .card-name{
                color: black;
            }
            .card-name{
                color: #888;
                font-weight: 600;
                text-align: center;

            }
            .cards .card:hover .icon-box{
                color: #fff;
            }



            .btn_ajouter{
                text-align: right;
            }
            .btn_ajouter a{
                margin-right: 35px;
            }
            .btn_ajouter a i{
                font-size: 30px;
                font-weight: bold;
            }



            .icon_sup{
                text-align: right;
            }
            .icon_sup i{
                color: black;
                font-size: 23px;
            }
            .card-name:hover{
                color: black;
            }
            .emoji{
                margin-top: 15px;
                display: grid;
                grid-template-columns: repeat(3,1fr);
                width: 100%;

            }
            .emoji p{
                text-align: center;
                display: flex;
                flex-direction: column;
            }
            .emoji p span{
                font-size: 16px;
                font-weight: bold;
            }
            .emoji i{
                font-size: 30px;
                align-self: center;
                margin-bottom: 10px;
            }
            .fa-smile{
                color: green;
            }
            .fa-meh{
                color: #666;
            }
            .fa-frown{
            
                color: red;
            }
            /* graphiques */
            .charts{
                display: grid;
                grid-template-columns:2fr 1fr ;
                grid-gap:20px;
                width: 100%;
                padding: 15px 0;
                padding-top: 0;
                margin-top: 10px;
            }
            .chart{
                background: #fff;
                padding: 20px;
                border-radius:10px;
                box-shadow: 0 7px 25px rgba(0,0,0,0.08);
                width: 100%;

            }
            canvas{
                max-height: 300px;

            }
            .chart h2{
                margin-bottom: 5px;
                font-size: 20px;
                color: #666;
                text-align: center;
            }
            .admin{
            visibility: hidden;
            cursor: none;
            }
            img{
                height: 50rem;
                width: 50rem;
                border-radius: 50%;
            }

            /* rendre responsive */
            @media(max-width:1115px){
                .sidebar{
                    width: 60px;
                }
                .main{
                    width: 100%;
                }
            }

            @media(max-width:880px){
                .cards{     
                    grid-template-columns: repeat(2, 1fr);    
                }
                .charts{
                    grid-template-columns: 1fr ;
                }


                .chart{
                    width: 99%;
                }
                
            
                #doughnut-chart{
                    padding: 50px;
                }
                #cercle{
                    padding: 50px;
                }
            }
            @media(max-width:500px){
                .topbar{
                    grid-template-columns: 1fr 5fr 0.4fr 1fr;    

                }
                .cards{     
                    grid-template-columns: 1fr;    
                    padding: 0;
                    margin: 0;
                }
                .logo h2{
                    font-size: 20px;
                }
                .search{
                    width: 80%;
                }
                .search input{
                    padding: 0 20px;
                }
                .fa-bell{
                    margin-right: 5px;
                }
                .user{
                    width: 40px;
                    height: 40px;
                }
                .chart{
                    width: 99%;
                }
                #doughnut-chart{
                    padding: 30px;
                
                }
                #cercle{
                    padding: 0;
                }
            }
    """

register_ = REGISTER()

login_ = LOGIN()