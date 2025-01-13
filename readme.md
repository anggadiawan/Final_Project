Sebelum run jangan lupa di aktifkan .venv dan install requirements dulu di 
    .venv\Scripts\activate
    pip install -r requirements.txt

Dalam tugas akhir ada terdapat dua file python:
    1. generate.py
        Generate.py bertujuan untuk engambil data dari elsevier menggunakan API, kemudian mengolah data tersebut menjadi format yang sesuai dengan kebutuhan tugas akhir.
        API yang digunakan itu 'a355a6131270ca7a9a07fc7b1226a671'
        nanti juga akan diminta inst token tapi dikosongkan saja sehingga klik enter saja.

        Data articles yang diambil itu dari 3 jurnal yaitu Structures, Engineering Structures, dan Building and Environments

    2. analyze.py
        analyze.py bertujuan untuk mengolah data yang telah diolah dari generate.py dengan cara mentokenisasi judul menjadi theme, subtheme, and subsubtheme. Pada file ini juga berisi untuk mengolah data tersebut menjadi chart yang dapat dilihat.

        Chart yang akan keluar adalah chat yang menunjukkan perbandingan antara theme, subtheme, dan subsubtheme setiap tahun dari setiap jurnal.

