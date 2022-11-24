(function() {
  let window = this;
  let randInt = function randInt(n) {
    return Math.floor(Math.random() * n);
  };

  let Problem = {
    init: function init(options) {
      let problem_start_time = null;
      let game = $("#game");
      let time_rem = game.find(".left");
      let score = game.find(".score");
      let banner = game.find(".banner");
      let problem = game.find(".problem");
      let answer = game.find(".answer");
      let body = $("body");
      answer.focus();

      /*
      let randGen = function randGen(minVal, maxVal) {
        return function() {
          return minVal + randInt(maxVal - minVal + 1);
        };
      };
      */
     let randGen = (minVal, maxVal) => minVal + randInt(maxVal - minVal + 1);

      if (options["num_type"] == "sino") {
        ranges = [[[2, 100], [2, 100]], [[2, 12], [2, 100]]];
      }

      let convert_to_korean = function convert_to_korean(num) {
        if (num == 0) {
          return "영";
        }
        digits = [
          "error",
          "일",
          "이",
          "삼",
          "사",
          "오",
          "육",
          "칠",
          "팔",
          "구"
        ];
        powers_of_ten = [
          "",
          "십",
          "백",
          "천",
          "만"
        ];

        out = "";
        for (let i = powers_of_ten.length - 1; i >= 0; i--) {
          place = 10 ** i;
          dig = Math.floor(num / place);
          num -= place * dig;
          if (dig == 0) {
            continue;
          }
          if (dig == 1) {
            if (i == 0) {
              out += digits[dig];
            }
            else {
              out += powers_of_ten[i];
            }
          }
          else {
            out += digits[dig] + powers_of_ten[i];
          }
        }
        return out;
      }
      
      let probAddSub = function probAddSub(add, kor=true) {
        let n0 = randGen(ranges[0][0][0], ranges[0][0][1])
        let n1 = randGen(ranges[0][1][0], ranges[0][1][1])
        let sm = n0 + n1;
        if (kor) {
          n0 = convert_to_korean(n0);
          n1 = convert_to_korean(n1);
          sm = convert_to_korean(sm);
        }
        return add ? [n0 + ' + ' + n1, sm] : [sm + ' \u2013 ' + n0, n1];
      };

      let probMultDiv = function probMultDiv(mult, kor=true) {
        let n0 = randGen(ranges[1][0][0], ranges[1][0][1])
        let n1 = randGen(ranges[1][1][0], ranges[1][1][1])
        let pd = n0 * n1;
        if (kor) {
          n0 = convert_to_korean(n0);
          n1 = convert_to_korean(n1);
          pd = convert_to_korean(pd);
        }
        return mult ? [n0 + ' \xD7 ' + n1, pd] : [pd + ' \xF7 ' + n0, n1];
      };

      subProbGens = [probAddSub, probMultDiv];
      let probGen = function probGen() {
        let out = null;
        while (out == null) {
          out = subProbGens[randInt(2)](randInt(2))
        }
        return out;
      };

      let curProb = null;
      let newProbSetup = function newProbSetup() {
        curProb = probGen();
        problem.text(curProb[0]);
        answer.val("");
      };

      let start_time = (problem_start_time = Date.now());
      let correct_ct = 0;
      let gameUpdate = function gameUpdate(e) {
        if ($.trim($(this).val()) === curProb[1] + '') {
          let now = Date.now();
          problem_start_time = now;
          newProbSetup();
          score.text("Score: " + ++correct_ct);
        }
        return true;
      };
      answer.keydown(gameUpdate).keyup(gameUpdate);
      newProbSetup(); 

      let duration = options.duration || 120;
      time_rem.text("Seconds left: " + duration);
      let timer = setInterval(function() {
        var d = duration - Math.floor((Date.now() - start_time) / 1000);
        time_rem.text("Seconds left: " + d);

        if (d <= 0) {
          answer.prop('disabled', true);
          clearInterval(timer);
          
          banner.find(".start").hide();
          banner.find(".end").show();
        }
      }, 1000);
    }
  };

  window.Problem = Problem;
}).call(this);