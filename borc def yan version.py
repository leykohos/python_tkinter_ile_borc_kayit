import tkinter as tk
from tkinter import messagebox
import sqlite3

# SQLite veritabanı bağlantısı oluşturma
conn = sqlite3.connect('veresiye_defteri.db')
cursor = conn.cursor()

# Veritabanı tablosunu oluşturma (Eğer daha önce oluşturulmamışsa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS veresiye (
        id INTEGER PRIMARY KEY,
        musteri_adi TEXT,
        urun_adi TEXT,
        miktar REAL,
        fiyat REAL
    )
''')
conn.commit()

# Ekleme işlemini gerçekleştiren fonksiyon
def ekle():
    musteri_adi = musteri_adi_entry.get()
    urun_adi = urun_adi_entry.get()
    miktar = miktar_entry.get()
    fiyat = fiyat_entry.get()

    if musteri_adi and urun_adi and miktar and fiyat:
        cursor.execute("INSERT INTO veresiye (musteri_adi, urun_adi, miktar, fiyat) VALUES (?, ?, ?, ?)", (musteri_adi, urun_adi, miktar, fiyat))
        conn.commit()
        listebox.insert(tk.END, f"{musteri_adi} - {urun_adi} - {miktar} - {fiyat}")
        temizle()
    else:
        messagebox.showerror("Hata", "Tüm alanları doldurun!")

# Borç silme işlemini gerçekleştiren fonksiyon
def borc_sil():
    secili_index = listebox.curselection()  # Seçilen öğenin indeksi
    if secili_index:
        secili_index = secili_index[0]  # İlk seçili öğenin indeksi
        secili_id = listebox.get(secili_index).split()[0]  # Seçili öğenin ilk kelimesini (ID'yi) al
        cursor.execute("DELETE FROM veresiye WHERE id=?", (secili_id,))
        conn.commit()
        listebox.delete(secili_index)  # Listeden seçili öğeyi sil

# Borçları gösterme işlemini gerçekleştiren fonksiyon
def borclari_goster():
    listebox.delete(0, tk.END)  # Liste kutusunu temizle

    cursor.execute("SELECT * FROM veresiye")
    rows = cursor.fetchall()
    for row in rows:
        listebox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")

# Temizleme işlemini gerçekleştiren fonksiyon
def temizle():
    musteri_adi_entry.delete(0, tk.END)
    urun_adi_entry.delete(0, tk.END)
    miktar_entry.delete(0, tk.END)
    fiyat_entry.delete(0, tk.END)

# Borçları arama işlemini gerçekleştiren fonksiyon
def borc_ara():
    aranan_musteri = musteri_ara_entry.get()
    listebox.delete(0, tk.END)  # Liste kutusunu temizle

    cursor.execute("SELECT * FROM veresiye WHERE musteri_adi LIKE ?", ('%' + aranan_musteri + '%',))
    rows = cursor.fetchall()
    for row in rows:
        listebox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")

# Ana uygulama penceresini oluştur
app = tk.Tk()
app.title("Kent Medikal Borç Defteri")  # Pencere başlığını değiştirin

# Sol Frame (Ekleme alanı)
sol_frame = tk.Frame(app)
sol_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Müşteri Adı etiket ve giriş kutusu
musteri_adi_label = tk.Label(sol_frame, text="Müşteri Adı:")
musteri_adi_label.pack()
musteri_adi_entry = tk.Entry(sol_frame)
musteri_adi_entry.pack()

# Ürün Adı etiket ve giriş kutusu
urun_adi_label = tk.Label(sol_frame, text="Ürün Adı:")
urun_adi_label.pack()
urun_adi_entry = tk.Entry(sol_frame)
urun_adi_entry.pack()

# Miktar etiket ve giriş kutusu
miktar_label = tk.Label(sol_frame, text="Miktar:")
miktar_label.pack()
miktar_entry = tk.Entry(sol_frame)
miktar_entry.pack()

# Fiyat etiket ve giriş kutusu
fiyat_label = tk.Label(sol_frame, text="Fiyat:")
fiyat_label.pack()
fiyat_entry = tk.Entry(sol_frame)
fiyat_entry.pack()

# Ekle düğmesi
ekle_button = tk.Button(sol_frame, text="Ekle", command=ekle)
ekle_button.pack()

# Borç Sil düğmesi
sil_button = tk.Button(sol_frame, text="Borç Sil", command=borc_sil)
sil_button.pack()

# Sağ Frame (Liste kutusu)
sag_frame = tk.Frame(app)
sag_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Borçları Göster düğmesi
goster_button = tk.Button(sag_frame, text="Borçları Göster", command=borclari_goster)
goster_button.pack()

# Liste kutusu
listebox = tk.Listbox(sag_frame, width=50, height=10)
listebox.pack()

# Borç arama kutusu ve düğmesi
musteri_ara_label = tk.Label(sag_frame, text="Müşteri Ara:")
musteri_ara_label.pack()
musteri_ara_entry = tk.Entry(sag_frame)
musteri_ara_entry.pack()
ara_button = tk.Button(sag_frame, text="Ara", command=borc_ara)
ara_button.pack()

# Uygulamayı çalıştır
app.mainloop()