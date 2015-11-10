$( document ).ready(function() {

    $("#tc-share").click(function(){

        var base_url = $("#base_url").val();
        var contestType = $("#contest_type").val();
        var update_date = $("#updated_date").val();
        var update_date_human = $("#updated_date_human").val();
        var picture = base_url +'/static/ratings-img/' + contestType + "_" + update_date + "-thumb.png";
        var link = base_url + '/ratings/' + contestType + "/" + update_date;
        var caption = 'Topcoder ratings ';
        var description = 'Ratings taken on the ' + update_date_human;

        share_facebook(link, picture, caption, description);
    });


    //var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    //po.src = 'https://apis.google.com/js/plusone.js';
    //var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
});