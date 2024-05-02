import { Inter } from "next/font/google";
import {Button, Upload} from "antd";
import {useState} from "react";
import proto from "@/grpc/service_grpc_web_pb";
import {toast, Toaster} from "react-hot-toast";


const inter = Inter({ subsets: ["latin"] });


// eepy
const grpcClient = new proto.WatermarkServiceClient("/api", null, null);

const getBase64 = (img, callback) => {
    try {
        const reader = new FileReader();
        reader.addEventListener('load', () => callback(btoa(reader.result)));
        // reader.readAsDataURL(img);
        // reader.readAsArrayBuffer()
        reader.readAsBinaryString(img)
    } catch (e) {
        console.log(e, img)
    }
};

export default function Home() {

    const [image, setImage] = useState({original: null, watermark: null});
    const [result, setResult] = useState(null)

    const isPic = (f) => ( f.type === "image/png")

    const wassermark = () => {
        const req = new proto.AddWatermarkRequest()
        req.setImage(image.original)
        req.setWatermark(image.watermark)

        console.log(image)

        grpcClient.addWatermark(req, null, (err, resp)=>{
            if (err) {
                toast(err.message||err)
                return
            }


            setResult(String.fromCharCode(...resp.getImage_asU8()))
            console.log(String.fromCharCode(...resp.getImage_asU8()))
        })

        // const watermarked = grpcClient.addWatermark()
    }

    return (
    <main className={`flex min-h-screen flex-col items-center justify-center p-4 gap-4 color-white ${inter.className}`}>
        <Toaster />
        <p className="font-slav text-8xl uppercase">фотошоп православный ☦️</p>
        <span className="font-slav text-5xl w-2/3">
            Добрый молодец иль дева, славься! Коли тебе Перун доверил изгнать ящеров нечестивых из редакции &quot;Славянского вестника&quot;
            плодящих ложь злостную. Ставь &quot;Ватермарки&quot; чтобы защитить печать на руси и не дать иродам окаянным украсть наш материал!
        </span>
        <div className={`${result?"max-w-2/3":"h-96 aspect-video"} bg-slate-900 rounded-xl border-2 border-white`}>
            {result && <img src={`data:image/jpeg;base64,${btoa(result)}`} className="rounded-xl" /> }
        </div>
        <div className="flex gap-8 items-center">
            <Upload name="Изображение" showUploadList={false}
                    beforeUpload={(f)=>{isPic(f)||toast("Неверное PNG изображение"); return isPic(f)}}
                    listType="picture-card" maxCount={1}
                    onChange={(info) => getBase64(info.file.originFileObj,
                        (img) => setImage({
                            ...image,
                            original: img,
                            originalPreview: `data:image/jpeg;base64,${img}`
                        }))}>
                {image.original ? <img src={image.originalPreview} alt="Изображение" className="rounded-lg"/> :
                    <span className="text-white">Выберите изображение (.PNG)</span>}
            </Upload>
            <span className="text-bold text-6xl">+</span>
            <Upload name="Ватермарка" showUploadList={false}
                    beforeUpload={(f)=>{isPic(f)||toast("Неверное PNG изображение"); return isPic(f)}}
                    listType="picture-card" maxCount={1}
                    onChange={(info) => getBase64(info.file.originFileObj,
                        (img) => setImage({
                        ...image,
                        watermark: img,
                        watermarkPreview: `data:image/jpeg;base64,${img}`
                    }))}>
                {image.watermark ? <img src={image.watermarkPreview} alt="Изображение" className="rounded-lg"/> :
                    <span className="text-white">Выберите ватермарку (.PNG)</span>}
            </Upload>
            <span className="text-bold text-3xl">→</span>
            <Button type="primary" onClick={wassermark}>Добавить ватермарку</Button>
        </div>
    </main>
  );
}
