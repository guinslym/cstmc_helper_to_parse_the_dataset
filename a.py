final_list=[]
b =[]
# You don't need `a` to be a list here, just iterate the `range` object
for num in range(13):
    if len(b) < 3:
        b.append(num)
    else:
        # Add `b` to `final_list` here itself, so that you don't have
        # to check if `b` has 3 elements in it, later in the loop.
        final_list.append(b)

        # Since `b` already has 3 elements, create a new list with one element
        b = [num]

# `b` might have few elements but not exactly 3. So, add it if it is not empty
if len(b) != 0:
    final_list.append(b)

print(final_list)
