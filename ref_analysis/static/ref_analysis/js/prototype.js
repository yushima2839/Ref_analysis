$(function(){

    // 始めるボタン押下時のイベント
  $("#startButton").on("click", function(){
      $("#overlay").fadeIn(200);
      $("#searchCondition").fadeIn(200);
  });

  //検索画面の閉じるボタン押下時のイベント
  $("#overlay, #closeSearch").on("click", function() {
        $("#overlay").fadeOut(200);
        $("#searchCondition").fadeOut(200, function() {
            $(this).removeClass("show");
        });
    })
    // カテゴリプルダウン押下時のイベント
    $("#categorySelect").on("change", function(){
        $("#teamSelect").prop("disabled", false)
    })

    // プルダウン変更時のイベント
    $("#categorySelect").on("change", function(){
        $("#categorySelect").css("color", "black")
        const league = $(this).val();
        // 下のプルダウン全て隠す
        $("#teamSelect option").hide();
        // プレースホルダだけ表示
        $("#teamSelect option[value='']").show();
        // 選ばれたリーグのチームだけ表示
        $("#teamSelect option." + league).show();
        // 選択をプレースホルダに戻す
        $("#teamSelect").prop("selectedIndex", 0);
    })

    $("#teamSelect").on("change", function(){
        $("#teamSelect").css("color", "black")
    })
    $("#refereeSelect").on("change", function(){
        $("#refereeSelect").css("color", "black")
    })
    $("#termSelect").on("change", function(){
        $("#termSelect").css("color", "black")
    })

    $('.gameResult').each(function () {
        const $scores = $(this).find('.score');

        const left = Number($scores.eq(0).text());
        const right = Number($scores.eq(1).text());

        $scores.removeClass('lose');

        if (left > right) {
            $scores.eq(1).addClass('lose');
        } else if (right > left) {
            $scores.eq(0).addClass('lose');
        } else if (left === right) {
            $scores.addClass('lose');
        }
        
    });
})