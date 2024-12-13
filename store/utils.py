from django.http import HttpResponse


def server_running(request):
    content = """
    <html>
    <head>
        <style>
            body {
                  background: linear-gradient(
                    to right,
                    #6f7280,
                    #2a2c3c,
                    #181827,
                    #833ab4,
                    #fd1d1d,
                    #fcb045
                );
                background-size: 400% 400%;
                animation: body 10s infinite ease-in-out;

            }
            h1 {
                font-family: system-ui;
                color: black;
                font-size: 30px;
                text-align: center;
                margin-top: 50px;
                margin-top: 50px;
            }
            p{
                text-align: center;
                font-size: 2rem;
            }
            div{
                margin-top:100px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            h5{
                text-align: center;
                color: darkolivegreen;
            }
            
            @keyframes body {
            0% {
                background-position: 0 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0 50%;
            }
            }

        </style>
    </head>
    <body>
    <div>
    	<img src="https://vms.arez.io/images/logos/favicon_512x512.png">
        </div>
        <h1>Store MGT server is online and operational.</h1> 
        <h5 class="text-center">V 3.10</h5>
    </body>
    </html>

    """
    return HttpResponse(content)


