// menghasilkan rincian penyewaan untuk check sebelum pelanggan benar-benar menyewa
function check()
{
    kuantitas = document.getElementById("kuantitas").value;
    tanggal_pengembalian = document.getElementById("tanggal_pengembalian").value;

    document.getElementById("konfirmasi_Username").innerHTML  = document.getElementById("username").value;
    document.getElementById("konfirmasi_Nama").innerHTML      = document.getElementById("nama").value;
    document.getElementById("konfirmasi_Judul").innerHTML     = document.getElementById("judul").value;
    document.getElementById("konfirmasi_Kuantitas").innerHTML = kuantitas;
    document.getElementById("konfirmasi_Tanggal").innerHTML   = tanggal_pengembalian;
    document.getElementById("konfirmasi_Total").innerHTML     = "Rp" + (30000 * kuantitas).toLocaleString();

    document.getElementById("conff").style.display = "block";
}

function metode_bayar()
{
    pilihan = document.getElementById("pilih_metode_pembayaran");
    display_cetak_nota = document.getElementById("cetaknotanow").style.display = "block";
    display_qrcode = document.getElementById("qrcode").style.display = "inline";

    if (pilihan.value == "Tunai")
    {
        alert("Permintaan Diterima, silahkan bawa Nota menuju ke Kasir untuk melakukan pembayaran :)");
        display_cetak_nota;
    }
    else if ((pilihan.value == "Debit") || (pilihan.value == "Kredit"))
    {
        alert("Permintaan Diterima, silahkan bawa Nota menuju ke Kasir untuk dipandu melakukan pembayaran menggunakan mesin EDC :)");
        display_cetak_nota;
    }
    else
    {
        alert("Permintaan Diterima, silahkan scan QRCODE di bawah, kemudian bawa nota ke kasir untuk mengambil DVD :)");
        display_qrcode;
        display_qrcodes;
        display_cetak_nota;
    }
}