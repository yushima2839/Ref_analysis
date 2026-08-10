$(function(){

    // sessionStorageにデータがあれば復帰
    const category = sessionStorage.getItem("category")
    const team_id = sessionStorage.getItem("team_id");
    const referee_id = sessionStorage.getItem("referee_id");
    const term = sessionStorage.getItem("term");




    if(category){
        $("#categorySelect").val(category);
        $("#teamSelect").prop("disabled", false); //チーム選択のdisabled解除
        // 復帰したカテゴリのチームだけ表示
        $("#teamSelect option").hide();
        $("#teamSelect option." + $("#categorySelect").val()).show();
    }

    if(team_id){
        $("#teamSelect").val(team_id);
    }

    if(referee_id){
        $("#refereeSelect").val(referee_id);
    }

    if(term){
        $("#termSelect").val(term);
    }
    if(sessionStorage.getItem("searchBack") == "true"){
        // オーバーレイ表示
        $("#overlay").fadeIn(200);
        $("#searchCondition").fadeIn(200);
        // F5復帰防止
        sessionStorage.removeItem("searchBack");
        sessionStorage.removeItem("category");
        sessionStorage.removeItem("team_id");
        sessionStorage.removeItem("referee_id");
        sessionStorage.removeItem("term");
        sessionStorage.removeItem("searchBack");
    }


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

    // プルダウン変更時のイベント
    $("#categorySelect").on("change", function(){
        $("#teamSelect").prop("disabled", false)
        $("#categorySelect").css("color", "#102040")
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
        $("#teamSelect").css("color", "#102040")
    })
    $("#refereeSelect").on("change", function(){
        $("#refereeSelect").css("color", "#102040")
    })
    $("#termSelect").on("change", function(){
        $("#termSelect").css("color", "#102040")
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

    // 検索ボタン押下時のイベント
    $("btn-neomorph-dark").on('click', function(){
        const button = $(this).find("button[type='submit']");

        // 2回目以降を防止
        if ($button.prop("disabled")) {
            return false;
        }

        $button.prop("disabled", true);
    })

    // 検索条件サブミットのイベント
    $('#searchForm').on('submit', function(e){
        const category = $('#categorySelect').val();
        const team = $('#teamSelect').val();
        const referee = $('#refereeSelect').val();
        const term =$('#termSelect').val();
        
        // 検索条件をsession storageに保存(復帰用)
        sessionStorage.setItem("searchBack", "true");
        sessionStorage.setItem("category", category);
        sessionStorage.setItem("team_id", team);
        sessionStorage.setItem("referee_id", referee);
        sessionStorage.setItem("term", term);
        
        console.log(category, team, referee, term);
        // 検索条件の空チェック
        if(!category || !team || !referee || !term ){
            e.preventDefault();
            $("#errorPopup").fadeIn(200);
            $("#errorOverlay").fadeIn(200);
        }
    })

    // ポップアップの閉じる処理
    $("#errorClose").on("click", function(){
        $("#errorPopup").fadeOut(200);
        $("#errorOverlay").fadeOut(200);
    });
})