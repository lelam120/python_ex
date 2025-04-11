import json
import os


class TaiLieu:
    def __init__(self, tieu_de, tac_gia):
        self.tieu_de = tieu_de
        self.tac_gia = tac_gia

    def __str__(self):
        return f"Tiêu đề: {self.tieu_de}, Tác giả: {self.tac_gia}"



class Sach(TaiLieu):
    def __init__(self, tieu_de, tac_gia, nam_xuat_ban, so_luong, con_lai=None):
        super().__init__(tieu_de, tac_gia)
        self.nam_xuat_ban = nam_xuat_ban
        self.so_luong = so_luong
        self.con_lai = con_lai if con_lai is not None else so_luong

    def __str__(self):
        return f"{super().__str__()}, Năm: {self.nam_xuat_ban}, Số lượng: {self.so_luong}, Còn lại: {self.con_lai}"

    def __hash__(self):
        return hash((self.tieu_de.lower(), self.tac_gia.lower(), self.nam_xuat_ban))

    def __eq__(self, other):
        return (self.tieu_de.lower(), self.tac_gia.lower(), self.nam_xuat_ban) == \
               (other.tieu_de.lower(), other.tac_gia.lower(), other.nam_xuat_ban)

    def to_dict(self):
        return {
            "tieu_de": self.tieu_de,
            "tac_gia": self.tac_gia,
            "nam_xuat_ban": self.nam_xuat_ban,
            "so_luong": self.so_luong,
            "con_lai": self.con_lai
        }

    @staticmethod
    def from_dict(du_lieu):
        return Sach(
            du_lieu["tieu_de"],
            du_lieu["tac_gia"],
            du_lieu["nam_xuat_ban"],
            du_lieu["so_luong"],
            du_lieu["con_lai"]
        )



class ThuVien:
    def __init__(self, duong_dan="thu_vien.json"):
        self.danh_sach_sach = set()
        self.duong_dan = duong_dan
        self.tai_du_lieu()

    def tai_du_lieu(self):
        if os.path.exists(self.duong_dan):
            try:
                with open(self.duong_dan, 'r', encoding='utf-8') as f:
                    du_lieu = json.load(f)
                    for sach_dict in du_lieu:
                        self.danh_sach_sach.add(Sach.from_dict(sach_dict))
            except Exception as e:
                print("Lỗi khi đọc file JSON:", e)

    def luu_du_lieu(self):
        try:
            with open(self.duong_dan, 'w', encoding='utf-8') as f:
                json.dump([sach.to_dict() for sach in self.danh_sach_sach], f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Lỗi khi lưu file JSON:", e)

    def tim_sach(self, tieu_de):
        for sach in self.danh_sach_sach:
            if sach.tieu_de.lower() == tieu_de.lower():
                return sach
        return None

    def them_sach(self):
        try:
            tieu_de = input("Nhập tiêu đề sách: ")
            tac_gia = input("Nhập tên tác giả: ")
            nam_xuat_ban = int(input("Nhập năm xuất bản: "))
            so_luong = int(input("Nhập số lượng: "))

            if so_luong <= 0:
                print("Số lượng phải lớn hơn 0. (Tạm gán = 1)")
                so_luong = 1

            sach_moi = Sach(tieu_de, tac_gia, nam_xuat_ban, so_luong)
            sach_co_san = self.tim_sach(tieu_de)

            if sach_co_san:
                sach_co_san.so_luong += so_luong
                sach_co_san.con_lai += so_luong
                print("Đã cập nhật số lượng sách.")
            else:
                self.danh_sach_sach.add(sach_moi)
                print("Đã thêm sách mới vào thư viện.")

            self.luu_du_lieu()
        except ValueError:
            print("Dữ liệu không hợp lệ. Vui lòng nhập lại.")

    def tim_kiem_sach(self):
        tieu_de = input("Nhập tiêu đề sách cần tìm: ")
        sach = self.tim_sach(tieu_de)
        if sach:
            print("Thông tin sách:")
            print(sach)
        else:
            print("Không tìm thấy sách.")

    def tim_sach_con_lai(self):
        tieu_de = input("Nhập tiêu đề sách cần tìm (chỉ hiện sách còn): ")
        sach = self.tim_sach(tieu_de)
        if sach and sach.con_lai > 0:
            print("Sách có sẵn:")
            print(sach)
        else:
            print("Không có sách sẵn trong thư viện.")

    def muon_sach(self):
        tieu_de = input("Nhập tiêu đề sách muốn mượn: ")
        sach = self.tim_sach(tieu_de)
        if sach:
            if sach.con_lai > 0:
                sach.con_lai -= 1
                print("Mượn sách thành công.")
            else:
                print("Sách đã hết, không thể mượn.")
        else:
            print("Không tìm thấy sách.")
        self.luu_du_lieu()

    def tra_sach(self):
        tieu_de = input("Nhập tiêu đề sách muốn trả: ")
        sach = self.tim_sach(tieu_de)
        if sach:
            if sach.con_lai < sach.so_luong:
                sach.con_lai += 1
                print("Trả sách thành công.")
            else:
                print("Tất cả sách đã đủ, không cần trả thêm.")
        else:
            print("Không tìm thấy sách.")
        self.luu_du_lieu()

    def hien_thi_tat_ca_sach(self):
        if not self.danh_sach_sach:
            print("Chưa có sách nào được thêm vào thư viện.")
            return
        print("\n Danh sách tất cả các sách trong thư viện:")
        for sach in self.danh_sach_sach:
            print(sach)

    def chay(self):
        while True:
            print("\n--- MENU ---")
            print("1. Thêm sách mới")
            print("2. Tìm kiếm sách theo tiêu đề")
            print("3. Tìm sách có sẵn")
            print("4. Mượn sách")
            print("5. Trả sách")
            print("6. Hiển thị tất cả sách")
            print("7. Thoát")

            try:
                lua_chon = input("Chọn chức năng (1-7): ")

                if lua_chon == '1':
                    self.them_sach()
                elif lua_chon == '2':
                    self.tim_kiem_sach()
                elif lua_chon == '3':
                    self.tim_sach_con_lai()
                elif lua_chon == '4':
                    self.muon_sach()
                elif lua_chon == '5':
                    self.tra_sach()
                elif lua_chon == '6':
                    self.hien_thi_tat_ca_sach()
                elif lua_chon == '7':
                    print("Đang lưu dữ liệu...")
                    self.luu_du_lieu()
                    print("Thoát chương trình.")
                    break
                else:
                    print("Bạn nhập không hợp lệ. Vui lòng chọn từ 1-7.")
            except Exception as loi:
                print("Lỗi không xác định:", loi)



if __name__ == "__main__":
    thu_vien = ThuVien()
    thu_vien.chay()
