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
                    try{
                        let title = movie_list[i].title;
                        let code = movie_list[i].code;
                        let temp_html = `
                                        <li><u><a onclick="print_movie(${code})" id="printmovie${i}" value="${code}">${title}</a></u></li>
                              `;
                        $('#movie_list').append(temp_html);
                    }catch (e){
                        
                    }
                    
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
            console.log(response);
            let movie_info = response.movie_info;
            let description = response.description;
            let outline = response.outline;
            let movie_img = response.img_url;
            let star_score = response.star_score;
            try {
                $('#movie_list').empty();
                $('.search_input').val('');
                
                $('#movie_img').attr('src',`${movie_img}`);
                $('#movie_title').text(`제목 : ${movie_info.title} ${movie_info.minititle}`);
                $('#movie_desc').text(`줄거리 : ${description.title}`);
                // $('#movie_desc').text(`줄거리 : ${description.content}`);
                $('#movie_date').text(`개봉날짜 : ${outline.release}`);
                $('#movie_rank').text(`평점 : ${star_score}`);
            } catch {
                alert('선택하신 영화의 정보가 올바르지 않습니다.');
                return window.location.href ='/';
            }
            


        }
    });
}





// {'movie_info': doc, 'outline':doc2,'actors':doc3,'img_url':img_url,'description':doc5,'star_score':data6}