//검색결과 실시간 통신
function send_keyword() {

    let keyword = $('.search_input').val();

    $.ajax({
        type: "POST",
        url: "/search_movie",
        data: {
            'keyword': keyword
        },
        success: function (response) {
            let msg = response.msg;
            let movie_list = response.movie;

            if (msg === 'o') {
                $('.search_input').empty();
                $('#btn-outline-success').attr('onclick',`print_movie(${movie_list[0].code})`);
                // for (let i = 0; i < movie_list.length; i++) {
                for (let i = 0; i < 5; i++) {
                    let title = movie_list[i].title;
                    let code = movie_list[i].code;
                    let temp_html = `
                                        <li><u><a onclick="print_movie(${code})" id="printmovie${i}" value="${code}">${title}</a></u></li>
                              `;
                    $('#movie_list').append(temp_html);
                }
            } else if (msg === '검색 결과가 없습니다.') {
                $('#movie_list').empty();
                let temp_html = `
                                    <li class='search none' style="list-style:none;">검색 결과가 없습니다.</li>
                              `;
                $('#movie_list').append(temp_html);
            }
        }
    });
}

//
function print_movie(code){
    $.ajax({
        type: "POST",
        url: "/print_movie",
        data: {
            'code': code
        },
        success: function (response) {
            let movie_info = response.movie_info;
            let description = response.description;
            let outline = response.outline;


            $('#movie_list').empty();
            $('.search_input').val('');
            console.log(response);

            $('#movie_title').text(`${movie_info.title} ${movie_info.minititle}`);
            $('#movie_desc').text(`${description.des_title}`);
            // $('#movie_desc').text(`줄거리 : ${description.des_content}`);
            $('#movie_date').text(`${outline.outline_release}`);
            $('#movie_rank').text(`평점 : 이미지 url이랑 같이 추가해야함`);


        }
    });
}





