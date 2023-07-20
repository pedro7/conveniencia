document.addEventListener("DOMContentLoaded", function(event) {
    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId)

        var sidebar = localStorage.getItem('sidebar');
        if (sidebar === null) {
            localStorage.setItem('sidebar', 'closed');
        }
        else if (sidebar === 'open') {
            nav.classList.add('l-navbar-fast')
            nav.classList.remove('l-navbar')
            nav.classList.toggle('show')
            toggle.classList.toggle('bx-x')
            bodypd.classList.toggle('body-pd')
            headerpd.classList.toggle('body-pd')
        }
    
    
        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
            var sidebar = localStorage.getItem('sidebar');
            if (sidebar === 'open') {
                localStorage.setItem('sidebar', 'closed');
            }
            else {
                localStorage.setItem('sidebar', 'open');
            }
            nav.classList.toggle('show')
            toggle.classList.toggle('bx-x')
            bodypd.classList.toggle('body-pd')
            headerpd.classList.toggle('body-pd')
            })
        }
    }
    showNavbar('header-toggle','nav-bar','body-pd','header')
});

function colorLink() {
    var currentURL = window.location.href;
    const linkColor = document.querySelectorAll('.nav_link')
    const links = []
    
    linkColor.forEach(function(l) {
        links.push(l)
    });

    if (currentURL.includes('colaboradores')) {
        links[1].classList.add('active')
    }
    else if (currentURL.includes('produtos')) {
        links[2].classList.add('active')
    }
    else if (currentURL.includes('estoque')) {
        links[3].classList.add('active')
    }
    else if (currentURL.includes('movimentacoes')) {
        links[4].classList.add('active')
    }
    else if (currentURL.includes('usuarios')) {
        links[5].classList.add('active')
    }
    else if (currentURL.includes('compras')) {
        links[6].classList.add('active')
    }
    else if (currentURL.includes('relatorios')) {
        links[7].classList.add('active')
    }
    else if (currentURL.includes('emails')) {
        links[8].classList.add('active')
    }
    else {
        links[0].classList.add('active')
    }
}

colorLink()