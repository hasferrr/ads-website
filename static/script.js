// menghasilkan rincian penyewaan untuk check sebelum pelanggan benar-benar menyewa
function check()
{
    let kuantitas = document.getElementById("kuantitas").value;
    let tanggal_pengembalian = document.getElementById("tanggal_pengembalian").value;

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
    selectElement = document.querySelector('#pilih_metode_pembayaran');
    pilihan = selectElement.options[selectElement.selectedIndex].value;

    if (pilihan == "Tunai")
    {
        alert("Permintaan Diterima, silahkan bawa Nota menuju ke Kasir untuk melakukan pembayaran :)");
        document.getElementById("cetaknotanow").style.display = "block";
    }
    else if ((pilihan == "Debit") || (pilihan == "Kredit"))
    {
        alert("Permintaan Diterima, silahkan bawa Nota menuju ke Kasir untuk dipandu melakukan pembayaran menggunakan mesin EDC :)");
        document.getElementById("cetaknotanow").style.display = "block";
    }
    else
    {
        alert("Permintaan Diterima, silahkan scan QRCODE di bawah, kemudian bawa nota ke kasir untuk mengambil DVD :)");
        document.getElementById("qrcode").style.display = "inline";
        document.getElementById("cetaknotanow").style.display = "block";
    }
}