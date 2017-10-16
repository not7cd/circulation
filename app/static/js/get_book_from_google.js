/**
 * Created by Akari on 5/5/16.
 */

(function () {
    function createMessage(message, type) {
        var type_convert = {
            'success': 'ok',
            'danger': 'ban-circle',
            'info': 'info-sign',
            'warning': 'alert'
        };

        var times = document.createElement('span');
        times.setAttribute('aria-hidden', 'true');
        times.textContent = '×';

        var button = document.createElement('button');
        button.setAttribute('type', 'button');
        button.setAttribute('data-dismiss', 'alert');
        button.setAttribute('aria-label', 'Close');
        button.classList.add('close');
        button.appendChild(times);

        var span = document.createElement('span');
        span.classList.add('glyphicon');
        span.classList.add('glyphicon-' + type_convert[type]);


        var container = document.createElement('div');
        container.setAttribute('role', 'alert');
        container.classList.add('alert');
        container.classList.add('alert-' + type);
        container.classList.add('alert-dismissible');
        container.appendChild(button);
        container.appendChild(span);
        container.innerHTML += ' ' + message;

        var main = document.querySelector('main');
        main.insertBefore(container, main.childNodes[0]);

    }

    document.getElementById('get_book_from_google').addEventListener('click', function () {
        var isbn = document.getElementById('isbn').value;

        if (isNaN(isbn) || isbn.length != 13) {
            createMessage('Please provide a 13-digit ISBN', 'warning');
        }
        else {
            $.getJSON("https://www.googleapis.com/books/v1/volumes?q=" + isbn)
                .done(function (data) {
                    // console.log(data.items[0].volumeInfo.categories);

                    if (data.code) {//There is a situation
                        if (data.code == '6000') {
                            createMessage('Book not found', 'danger');
                        }
                        else {
                            createMessage(data.msg, 'danger');
                        }
                    }
                    else {
                        document.getElementById('title').value = data.items[0].volumeInfo.title;
                        document.getElementById('subtitle').value = data.items[0].volumeInfo.subtitle;
                        document.getElementById('authors').value = data.items[0].volumeInfo.authors;
                        document.getElementById('publisher').value = data.items[0].volumeInfo.publisher;
                        document.getElementById('thumbnail').value = data.items[0].volumeInfo.imageLinks.thumbnail;
                        document.getElementById('publishedDate').value = data.items[0].volumeInfo.publishedDate;
                        document.getElementById('pageCount').value = data.items[0].volumeInfo.pageCount;
                        document.getElementById('flask-pagedown-summary').value = data.items[0].volumeInfo.description.replace(/\n/g, "\n\n");
                        createMessage('Fetch successful', 'success');
                    }
                })
                .fail(function (data) {
                    if (data.status == '404')
                        createMessage('Fetch unsuccessful!', 'danger');
                    else
                        createMessage(datas.tatusText, 'danger');
                });

        }
    }, false);
})();
