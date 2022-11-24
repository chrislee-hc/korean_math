import random
import time
import sys

def convert_to_sino(num):
  if type(num) is not int or num < 0 or num >= 100000:
    raise ValueError("Argument must be a nonnegative integer below 100k")
  
  if num == 0:
    return "영"
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
  ]
  powers_of_ten = [
    "",
    "십",
    "백",
    "천",
    "만"
  ]

  out = ""
  for i in range(4, -1, -1):
    place = int(10 ** i)
    dig = num // place
    num -= dig * place
    if dig == 0:
      continue
    if dig == 1:
      if i == 0:
        out += digits[dig]
      else:
        out += powers_of_ten[i]
    else:
      out += digits[dig] + powers_of_ten[i]

  return out

def convert_to_native(num):
  if type(num) is not int or num < 0 or num >= 100:
    raise ValueError("Argument must be a nonnegative integer below 100")
  
  ones = [
    "",
    "하나",
    "둘",
    "셋",
    "넷",
    "다섯",
    "여섯",
    "일곱",
    "여덟",
    "아홉",
  ]
  tens = [
    "",
    "열",
    "스물",
    "서른",
    "마흔",
    "쉰",
    "예순",
    "일흔",
    "여든",
    "아흔"
  ]

  return tens[num // 10] + ones[num % 10]

def get_math_problem(ops=None, sm_range=(2, 12), big_range=(2, 100), lim=None):
  if ops is None:
    ops = ["+", "-", "*", "/"]
  op = random.choice(ops)
  if lim is None:
    lim = sm_range[1] * big_range[1] + 1
  a = b = lim

  if op == "+":
    a = random.randint(*big_range)
    b = random.randint(*big_range)
    return (a, b, op, a+b)
  elif op == "-":
    while a == b:
      a = random.randint(*big_range)
      b = random.randint(*big_range)
    if b > a:
      a, b = b, a
    return (a, b, op, a-b)
  elif op == "*":
    while a * b >= lim:
      a = random.randint(*sm_range)
      b = random.randint(*big_range)
    return (a, b, op, a*b)
  elif op == "/":
    a = b = lim
    while a * b >= lim:
      a = random.randint(*sm_range)
      b = random.randint(*big_range)
    return (a*b, a, op, b)

def get_sino_math_problem(*args, **kwargs):
  a, b, op, ans = get_math_problem(*args, **kwargs)
  sino_a = convert_to_sino(a)
  sino_b = convert_to_sino(b)
  sino_ans = convert_to_sino(ans)
  return f"{sino_a} {op} {sino_b}", sino_ans

def get_native_math_problem(*args, **kwargs):
  a, b, op, ans = get_math_problem(*args, sm_range=(2, 10), big_range=(2, 10), lim=100, **kwargs)
  sino_a = convert_to_native(a)
  sino_b = convert_to_native(b)
  sino_ans = convert_to_native(ans)
  return f"{sino_a} {op} {sino_b}", sino_ans

def test_math(prob_gen, num_probs=10):
  start_time = time.time()
  guesses = 0
  for _ in range(num_probs):
    ques, ans = prob_gen()
    user_ans = ""
    while user_ans != ans:
      if user_ans != "":
        print("\033[91m" + "wrong" + "\033[0m")
      user_ans = input(f"{ques} = ")
      user_ans = "".join(c for c in user_ans if not c.isspace())
      guesses += 1
    print("\033[92m" + "correct" + "\033[0m")

  end_time = time.time()
  print('\033[94m\033[1m' + f"Total time:\t\t{int(end_time - start_time)} seconds" + '\033[0m')
  print('\033[94m\033[1m' + f"Average time:\t\t{(end_time - start_time) / num_probs :.2f} seconds / problem" + '\033[0m')
  print('\033[94m\033[1m' + f"Incorrect Entries:\t{guesses - num_probs} out of {num_probs} problems" + '\033[0m')


if __name__ == "__main__":
  if len(sys.argv) <= 2:
    print("Please specify the following arguments: sino/native, number of problems")
  elif sys.argv[1].lower().strip() == "native":
    test_math(get_native_math_problem, num_probs=int(sys.argv[2]))
  else:
    test_math(get_sino_math_problem, num_probs=int(sys.argv[2]))
#  for i in range(1, 100):
#    print(convert_to_native(i))

