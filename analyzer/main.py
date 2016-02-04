if __name__ == '__main__':
    # filename_list = get_filename()
    expenses = []
    # for filename in filename_list:
    for filename in get_all_data_files():
        expenses += meta_parser(filename)

    # for i in expenses:
    #     print(i)

    sorted_by_month = sort_expenses_by_month(expenses)
    sorted_list_by_month = sorted(sorted_by_month.items(), key=lambda x:x[0])

    for i in sorted_list_by_month:
        print('_'*10)
        print(i[0] + ': ' +str(sum_total_expenses(i[1])['expenses_sum']))
        print(display_sorted_categories(i[1]))
        # print(order_by_category(i[1], CATEGORIES))
    #display_sorted_categories(expenses)