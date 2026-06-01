from account import Account

class AccountDAO:
    def __init__(self):
        self.__accountDB = {}

    def insert_account(self, account):
        account_no = account.get_account_no()
        if account_no not in self.__accountDB:
            self.__accountDB[account_no] = account
            return True
        return False
    
    def select_account_by_account_no(self, account_no):
        if account_no in self.__accountDB:
            return self.__accountDB[account_no]
    def select_accounts_by_member_id(self, member_id):
        for account in self.__accountDB.values():
            if account.get_owner() == member_id:
                account_list.append(account)

        if len(account_list): return account_list
        return None
    def select_all_accounts(self):
        account_list = list(self.__accountDB.values())
        if len(account_list):
            return account_list
        return None
    def update_account(self, account_no, account)
            if account_no in self.__accountDB:
            self.__accountDB[account_no] = account
            return True
        return False
    def delete_account(self, account_no):
        pass

if __name__ == '__main__':
    dao = AccountDAO()
    ac_list = dao.select_all_accounts()
    print(ac_list)
    ac = Account('111111', 'ethan', 10000, '1234')
    dao.insert_account(Account('111111', 'ethan', 10000, '1234'))
    dao.insert_account(Account('121111', 'johnny', 10000, '1234'))
    for account in dao.select_all_accounts():
        print(account)
    print(dao.select_account_by_account_no('121111'))
    for account in dao.select_accounts_by_member_id('ethan'):
        print(account)
    dao.update_account('121111', Account('121111', 'johnny', 30000, '1234') )
    print(dao.select_account_b)