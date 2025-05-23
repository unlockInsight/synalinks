# License Apache 2.0: (c) 2025 Yoan Sallami (Synalinks Team)

import json
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

from synalinks.src.api_export import synalinks_export
from synalinks.src.backend import DataModel
from synalinks.src.utils import file_utils

from .dsl import Grid

BASE_URL = "https://raw.githubusercontent.com/fchollet/ARC-AGI/refs/heads/master/data/"

TRAINING_TASK_NAMES = [
    "007bbfb7",
    "00d62c1b",
    "017c7c7b",
    "025d127b",
    "045e512c",
    "0520fde7",
    "05269061",
    "05f2a901",
    "06df4c85",
    "08ed6ac7",
    "09629e4f",
    "0962bcdd",
    "0a938d79",
    "0b148d64",
    "0ca9ddb6",
    "0d3d703e",
    "0dfd9992",
    "0e206a2e",
    "10fcaaa3",
    "11852cab",
    "1190e5a7",
    "137eaa0f",
    "150deff5",
    "178fcbfb",
    "1a07d186",
    "1b2d62fb",
    "1b60fb0c",
    "1bfc4729",
    "1c786137",
    "1caeab9d",
    "1cf80156",
    "1e0a9b12",
    "1e32b0e9",
    "1f0c79e5",
    "1f642eb9",
    "1f85a75f",
    "1f876c06",
    "1fad071e",
    "2013d3e2",
    "2204b7a8",
    "22168020",
    "22233c11",
    "2281f1f4",
    "228f6490",
    "22eb0ac0",
    "234bbc79",
    "23581191",
    "239be575",
    "23b5c85d",
    "253bf280",
    "25d487eb",
    "25d8a9c8",
    "25ff71a9",
    "264363fd",
    "272f95fa",
    "27a28665",
    "28bf18c6",
    "28e73c20",
    "29623171",
    "29c11459",
    "29ec7d0e",
    "2bcee788",
    "2bee17df",
    "2c608aff",
    "2dc579da",
    "2dd70a9a",
    "2dee498d",
    "31aa019c",
    "321b1fc6",
    "32597951",
    "3345333e",
    "3428a4f5",
    "3618c87e",
    "3631a71a",
    "363442ee",
    "36d67576",
    "36fdfd69",
    "3906de3d",
    "39a8645d",
    "39e1d7f9",
    "3aa6fb7a",
    "3ac3eb23",
    "3af2c5a8",
    "3bd67248",
    "3bdb4ada",
    "3befdf3e",
    "3c9b0459",
    "3de23699",
    "3e980e27",
    "3eda0437",
    "3f7978a0",
    "40853293",
    "4093f84a",
    "41e4d17e",
    "4258a5f9",
    "4290ef0e",
    "42a50994",
    "4347f46a",
    "444801d8",
    "445eab21",
    "447fd412",
    "44d8ac46",
    "44f52bb0",
    "4522001f",
    "4612dd53",
    "46442a0e",
    "469497ad",
    "46f33fce",
    "47c1f68c",
    "484b58aa",
    "48d8fb45",
    "4938f0c2",
    "496994bd",
    "49d1d64f",
    "4be741c5",
    "4c4377d9",
    "4c5c2cf0",
    "50846271",
    "508bd3b6",
    "50cb2852",
    "5117e062",
    "5168d44c",
    "539a4f51",
    "53b68214",
    "543a7ed5",
    "54d82841",
    "54d9e175",
    "5521c0d9",
    "5582e5ca",
    "5614dbcf",
    "56dc2b01",
    "56ff96f3",
    "57aa92db",
    "5ad4f10b",
    "5bd6f4ac",
    "5c0a986e",
    "5c2c9af4",
    "5daaa586",
    "60b61512",
    "6150a2bd",
    "623ea044",
    "62c24649",
    "63613498",
    "6430c8c4",
    "6455b5f5",
    "662c240a",
    "67385a82",
    "673ef223",
    "6773b310",
    "67a3c6ac",
    "67a423a3",
    "67e8384a",
    "681b3aeb",
    "6855a6e4",
    "68b16354",
    "694f12f3",
    "6a1e5592",
    "6aa20dc0",
    "6b9890af",
    "6c434453",
    "6cdd2623",
    "6cf79266",
    "6d0160f0",
    "6d0aefbc",
    "6d58a25d",
    "6d75e8bb",
    "6e02f1e3",
    "6e19193c",
    "6e82a1ae",
    "6ecd11f4",
    "6f8cd79b",
    "6fa7a44f",
    "72322fa7",
    "72ca375d",
    "73251a56",
    "7447852a",
    "7468f01a",
    "746b3537",
    "74dd1130",
    "75b8110e",
    "760b3cac",
    "776ffc46",
    "77fdfe62",
    "780d0b14",
    "7837ac64",
    "794b24be",
    "7b6016b9",
    "7b7f7511",
    "7c008303",
    "7ddcd7ec",
    "7df24a62",
    "7e0986d6",
    "7f4411dc",
    "7fe24cdd",
    "80af3007",
    "810b9b61",
    "82819916",
    "83302e8f",
    "834ec97d",
    "8403a5d5",
    "846bdb03",
    "855e0971",
    "85c4e7cd",
    "868de0fa",
    "8731374e",
    "88a10436",
    "88a62173",
    "890034e9",
    "8a004b2b",
    "8be77c9e",
    "8d5021e8",
    "8d510a79",
    "8e1813be",
    "8e5a5113",
    "8eb1be9a",
    "8efcae92",
    "8f2ea7aa",
    "90c28cc7",
    "90f3ed37",
    "913fb3ed",
    "91413438",
    "91714a58",
    "9172f3a0",
    "928ad970",
    "93b581b8",
    "941d9a10",
    "94f9d214",
    "952a094c",
    "9565186b",
    "95990924",
    "963e52fc",
    "97999447",
    "97a05b5b",
    "98cf29f8",
    "995c5fa3",
    "99b1bc43",
    "99fa7670",
    "9aec4887",
    "9af7a82c",
    "9d9215db",
    "9dfd6313",
    "9ecd008a",
    "9edfc990",
    "9f236235",
    "a1570a43",
    "a2fd1cf0",
    "a3325580",
    "a3df8b1e",
    "a416b8f3",
    "a48eeaf7",
    "a5313dff",
    "a5f85a15",
    "a61ba2ce",
    "a61f2674",
    "a64e4611",
    "a65b410d",
    "a68b268e",
    "a699fb00",
    "a740d043",
    "a78176bb",
    "a79310a0",
    "a85d4709",
    "a87f7484",
    "a8c38be5",
    "a8d7556c",
    "a9f96cdd",
    "aabf363d",
    "aba27056",
    "ac0a08a4",
    "ae3edfdc",
    "ae4f1146",
    "aedd82e4",
    "af902bf9",
    "b0c4d837",
    "b190f7f5",
    "b1948b0a",
    "b230c067",
    "b27ca6d3",
    "b2862040",
    "b527c5c6",
    "b548a754",
    "b60334d2",
    "b6afb2da",
    "b7249182",
    "b775ac94",
    "b782dc8a",
    "b8825c91",
    "b8cdaf2b",
    "b91ae062",
    "b94a9452",
    "b9b7f026",
    "ba26e723",
    "ba97ae07",
    "bb43febb",
    "bbc9ae5d",
    "bc1d5164",
    "bd4472b8",
    "bda2d7a6",
    "bdad9b1f",
    "be94b721",
    "beb8660c",
    "c0f76784",
    "c1d99e64",
    "c3e719e8",
    "c3f564a4",
    "c444b776",
    "c59eb873",
    "c8cbb738",
    "c8f0f002",
    "c909285e",
    "c9e6f938",
    "c9f8e694",
    "caa06a1f",
    "cbded52d",
    "cce03e0d",
    "cdecee7f",
    "ce22a75a",
    "ce4f8723",
    "ce602527",
    "ce9e57f2",
    "cf98881b",
    "d037b0a7",
    "d06dbe63",
    "d07ae81c",
    "d0f5fe59",
    "d10ecb37",
    "d13f3404",
    "d22278a0",
    "d23f8c26",
    "d2abd087",
    "d364b489",
    "d406998b",
    "d43fd935",
    "d4469b4b",
    "d4a91cb9",
    "d4f3cd78",
    "d511f180",
    "d5d6de2d",
    "d631b094",
    "d687bc17",
    "d6ad076f",
    "d89b689b",
    "d8c310e9",
    "d90796e8",
    "d9f24cd1",
    "d9fac9be",
    "dae9d2b5",
    "db3e9e38",
    "db93a21d",
    "dbc1a6ce",
    "dc0a314f",
    "dc1df850",
    "dc433765",
    "ddf7fa4f",
    "de1cd16c",
    "ded97339",
    "e179c5f4",
    "e21d9049",
    "e26a3af2",
    "e3497940",
    "e40b9e2f",
    "e48d4e1a",
    "e5062a87",
    "e509e548",
    "e50d258f",
    "e6721834",
    "e73095fd",
    "e76a88a6",
    "e8593010",
    "e8dc4411",
    "e9614598",
    "e98196ab",
    "e9afcf9a",
    "ea32f347",
    "ea786f4a",
    "eb281b96",
    "eb5a1d5d",
    "ec883f72",
    "ecdecbb3",
    "ed36ccf7",
    "ef135b50",
    "f15e1fac",
    "f1cefba8",
    "f25fbde4",
    "f25ffba3",
    "f2829549",
    "f35d900a",
    "f5b8619d",
    "f76d97a5",
    "f8a8fe49",
    "f8b3ba0a",
    "f8c80d96",
    "f8ff0b80",
    "f9012d9b",
    "fafffa47",
    "fcb5c309",
    "fcc82909",
    "feca6190",
    "ff28f65a",
    "ff805c23",
]

EVALUATION_TASK_NAMES = [
    "00576224",
    "009d5c81",
    "00dbd492",
    "03560426",
    "05a7bcf2",
    "0607ce86",
    "0692e18c",
    "070dd51e",
    "08573cc6",
    "0934a4d8",
    "09c534e7",
    "0a1d4ef5",
    "0a2355a6",
    "0b17323b",
    "0bb8deee",
    "0becf7df",
    "0c786b71",
    "0c9aba6e",
    "0d87d2a6",
    "0e671a1a",
    "0f63c0b9",
    "103eff5b",
    "11e1fe23",
    "12422b43",
    "12997ef3",
    "12eac192",
    "136b0064",
    "13713586",
    "137f0df0",
    "140c817e",
    "14754a24",
    "15113be4",
    "15663ba9",
    "15696249",
    "16b78196",
    "17b80ad2",
    "17cae0c1",
    "18419cfa",
    "184a9768",
    "195ba7dc",
    "1990f7a8",
    "19bb5feb",
    "1a2e2828",
    "1a6449f1",
    "1acc24af",
    "1c02dbbe",
    "1c0d0a4b",
    "1c56ad9f",
    "1d0a4b61",
    "1d398264",
    "1da012fc",
    "1e81d6f9",
    "1e97544e",
    "2037f2c7",
    "2072aba6",
    "20818e16",
    "20981f0e",
    "212895b5",
    "21f83797",
    "22a4bbc2",
    "25094a63",
    "2546ccf6",
    "256b0a75",
    "2685904e",
    "2697da3f",
    "2753e76c",
    "27a77e38",
    "27f8ce4f",
    "281123b4",
    "292dd178",
    "29700607",
    "2a5f8217",
    "2b01abd0",
    "2c0b0aff",
    "2c737e39",
    "2f0c5170",
    "310f3251",
    "3194b014",
    "319f2597",
    "31adaf00",
    "31d5ba1a",
    "32e9702f",
    "332efdb3",
    "3391f8c0",
    "33b52de3",
    "3490cc26",
    "34b99a2b",
    "351d6448",
    "358ba94e",
    "37d3e8b2",
    "3979b1a8",
    "3a301edc",
    "3b4c2228",
    "3d31c5b3",
    "3ed85e70",
    "3ee1011a",
    "3f23242b",
    "40f6cd08",
    "414297c0",
    "423a55dc",
    "42918530",
    "42a15761",
    "4364c1c4",
    "456873bc",
    "45737921",
    "45bbe264",
    "477d2879",
    "47996f11",
    "48131b3c",
    "4852f2fa",
    "48f8583b",
    "4aab4007",
    "4acc7107",
    "4b6b68e5",
    "4c177718",
    "4cd1b7b2",
    "4e45f183",
    "4e469f39",
    "4f537728",
    "4ff4c9da",
    "505fff84",
    "506d28a5",
    "50a16a69",
    "50aad11f",
    "50f325b5",
    "516b51b7",
    "5207a7b5",
    "5289ad53",
    "52fd389e",
    "54db823b",
    "55059096",
    "551d5bf1",
    "55783887",
    "575b1a71",
    "5783df64",
    "5833af48",
    "58743b76",
    "58e15b12",
    "59341089",
    "5a5a2103",
    "5af49b42",
    "5b526a93",
    "5b692c0f",
    "5b6cbef5",
    "5d2a5c43",
    "5ffb2104",
    "604001fa",
    "60a26a3e",
    "60c09cac",
    "626c0bcc",
    "62ab2642",
    "62b74c02",
    "639f5a19",
    "642248e4",
    "642d658d",
    "64a7c07e",
    "66e6c45b",
    "66f2d22f",
    "67636eac",
    "67b4a34d",
    "67c52801",
    "68b67ca3",
    "692cd3b6",
    "695367ec",
    "696d4842",
    "69889d6e",
    "6a11f6da",
    "6ad5bdfd",
    "6df30ad6",
    "6ea4a07e",
    "6f473927",
    "7039b2d7",
    "705a3229",
    "712bf12e",
    "72207abc",
    "72a961c9",
    "73182012",
    "73c3b0d8",
    "73ccf9c2",
    "759f3fd3",
    "762cd429",
    "770cc55f",
    "782b5218",
    "79369cc6",
    "7953d61e",
    "79fb03f4",
    "7bb29440",
    "7c8af763",
    "7c9b52a0",
    "7d18a6fb",
    "7d1f7ee8",
    "7d419a02",
    "7e02026e",
    "7ee1c6ea",
    "817e6c09",
    "81c0276b",
    "833dafe3",
    "845d6e51",
    "84db8fc4",
    "84f2aca1",
    "8597cfd7",
    "85b81ff1",
    "85fa5666",
    "8719f442",
    "88207623",
    "891232d6",
    "896d5239",
    "8a371977",
    "8b28cd80",
    "8ba14f53",
    "8cb8642d",
    "8dae5dfc",
    "8e2edd66",
    "8ee62060",
    "8fbca751",
    "90347967",
    "903d1b4a",
    "9110e3c5",
    "917bccba",
    "929ab4e9",
    "92e50de0",
    "9356391f",
    "93b4f4b3",
    "93c31fbe",
    "94133066",
    "94414823",
    "94be5b80",
    "95a58926",
    "963f59bc",
    "96a8c0cd",
    "97239e3d",
    "9772c176",
    "981571dc",
    "992798f6",
    "99306f82",
    "9a4bb226",
    "9b2a60aa",
    "9b365c51",
    "9b4c17c4",
    "9bebae7a",
    "9c1e755f",
    "9c56f360",
    "9caba7c3",
    "9ddd00f0",
    "9def23fe",
    "9f27f097",
    "a04b2602",
    "a096bf4d",
    "a3f84088",
    "a406ac07",
    "a57f2f04",
    "a59b95c0",
    "a680ac02",
    "a8610ef7",
    "a934301b",
    "aa18de87",
    "aa300dc3",
    "aa4ec2a5",
    "aab50785",
    "ac0c5833",
    "ac2e8ecf",
    "ac3e2b04",
    "ac605cbb",
    "ad7e01d0",
    "ae58858e",
    "aee291af",
    "af22c60d",
    "af24b4cc",
    "b0722778",
    "b0f4d537",
    "b15fca0b",
    "b1fc8b8e",
    "b20f7c8b",
    "b457fec5",
    "b4a43f3b",
    "b7999b51",
    "b7cb93ac",
    "b7f8a4d8",
    "b7fb29bc",
    "b942fd60",
    "b9630600",
    "ba9d41b8",
    "baf41dbf",
    "bb52a14b",
    "bbb1b8b6",
    "bc4146bd",
    "bcb3040b",
    "bd14c3bf",
    "be03b35f",
    "bf32578f",
    "bf699163",
    "bf89d739",
    "c074846d",
    "c1990cce",
    "c3202e5a",
    "c35c1b4c",
    "c48954c1",
    "c62e2108",
    "c64f1187",
    "c658a4bd",
    "c663677b",
    "c6e1b8da",
    "c7d4e6ad",
    "c87289bb",
    "c8b7cc0f",
    "c92b942c",
    "c97c0139",
    "ca8de6ea",
    "ca8f78db",
    "cad67732",
    "cb227835",
    "ccd554ac",
    "cd3c21df",
    "ce039d91",
    "ce8d95cc",
    "cf133acc",
    "cfb2ce5a",
    "d017b73f",
    "d19f7514",
    "d282b262",
    "d2acf2cb",
    "d304284e",
    "d37a1ef5",
    "d47aa2ff",
    "d492a647",
    "d4b1c2b1",
    "d4c90558",
    "d56f2372",
    "d5c634a2",
    "d931c21c",
    "d94c3b52",
    "da2b0fe3",
    "da515329",
    "dc2aa30b",
    "dc2e9a9d",
    "dd2401ed",
    "de493100",
    "df8cc377",
    "e0fb7511",
    "e133d23d",
    "e1baa8a4",
    "e1d2900e",
    "e2092e0c",
    "e21a174a",
    "e345f17b",
    "e4075551",
    "e41c6fd3",
    "e57337a4",
    "e5790162",
    "e5c44e8f",
    "e619ca6e",
    "e633a9e5",
    "e66aafb8",
    "e681b708",
    "e69241bd",
    "e6de6e8f",
    "e74e1818",
    "e760a62e",
    "e7639916",
    "e78887d1",
    "e7a25a18",
    "e7b06bea",
    "e7dd8335",
    "e872b94a",
    "e88171ec",
    "e95e3d8e",
    "e99362f0",
    "e9ac8c9e",
    "e9b4f6fc",
    "e9bb6954",
    "e9c9d9a1",
    "ea959feb",
    "ea9794b1",
    "ecaa0ec1",
    "ed74f2f2",
    "ed98d772",
    "ef26cbf6",
    "f0afb749",
    "f0df5ff0",
    "f21745ec",
    "f3b10344",
    "f3cdc58f",
    "f3e62deb",
    "f4081712",
    "f45f5ca7",
    "f5aa3634",
    "f5c89df1",
    "f823c43c",
    "f83cb3f6",
    "f8be4b64",
    "f9a67cb5",
    "f9d67f8b",
    "fafd9572",
    "fb791726",
    "fc754716",
    "fd096ab6",
    "fd4b2b02",
    "fe9372f3",
    "fea12743",
    "ff72ca3e",
]


class TaskExample(DataModel):
    """An example of task"""

    inputs: Grid
    outputs: Grid


class ARCAGIInput(DataModel):
    """Input data model"""

    examples: List[TaskExample] = []
    grid: Grid


class ARCAGIOutput(DataModel):
    """Find the common rule that maps an input grid to an output grid."""

    grid: Grid


@synalinks_export("synalinks.datasets.arcagi.get_training_task_names")
def get_training_task_names():
    return TRAINING_TASK_NAMES


@synalinks_export("synalinks.datasets.arcagi.get_validation_task_names")
def get_validation_task_names():
    return EVALUATION_TASK_NAMES


@synalinks_export("synalinks.datasets.arcagi.get_task_names")
def get_task_names():
    return TRAINING_TASK_NAMES + EVALUATION_TASK_NAMES


@synalinks_export("synalinks.datasets.arcagi.get_input_data_model")
def get_input_data_model():
    """
    Returns ARC-AGI input data_model for pipeline configurations.

    Returns:
        (DataModel): The ARC-AGI input data_model
    """
    return ARCAGIInput


@synalinks_export("synalinks.datasets.arcagi.get_output_data_model")
def get_output_data_model():
    """
    Returns ARC-AGI output data_model for pipeline configurations.

    Returns:
        (DataModel): The ARC-AGI output data_model
    """
    return ARCAGIOutput


@synalinks_export("synalinks.datasets.arcagi.plot_task")
def plot_task(
    x=None,
    y_true=None,
    y_pred=None,
    task_name=None,
    to_file=None,
):
    """
    Plot a task for debugging purposes

    Code Example:

    ```python
    synlinks.datasets.arcagi.plot_task(task_name="025d127b")
    ```

    Example:

    ![025d127b](../../assets/025d127b.png)

    Args:
        x (DataModel): Optional. The task inputs.
        y_true (DataModel): Optional. The task target data.
        y_pred (DataModel): Optional. The prediction.
        task_name (str): The task name to fetch the data if not provided.
        to_file (str): The filepath where to save the figure.
    """
    if not x and not y_true and task_name:
        x, y_true = fetch_and_format(task_name)
        if not to_file:
            to_file = f"{task_name}.png"

    if not to_file:
        to_file = "arc_agi_task.png"

    cmap = colors.ListedColormap(
        [
            "#000000",
            "#0074D9",
            "#FF4136",
            "#2ECC40",
            "#FFDC00",
            "#AAAAAA",
            "#F012BE",
            "#FF851B",
            "#7FDBFF",
            "#870C25",
        ]
    )
    norm = colors.Normalize(vmin=0, vmax=9)

    nb_examples = len(x.examples)
    n = nb_examples + 1
    fig, axis = plt.subplots(2, n)

    for i, example in enumerate(x.examples):
        inputs, outputs = x.examples[i].inputs, x.examples[i].outputs
        inputs, outputs = np.array(inputs), np.array(outputs)

        axis[0, i].imshow(inputs, cmap=cmap, norm=norm)
        axis[0, i].set_title(f"x_train {i}")
        axis[0, i].grid(axis="both", color="white", linewidth=1)
        axis[0, i].set_yticks(np.arange(-0.5, inputs.shape[0], 1))
        axis[0, i].set_xticks(np.arange(-0.5, inputs.shape[1], 1))
        axis[0, i].set_yticklabels([])
        axis[0, i].set_xticklabels([])

        axis[1, i].imshow(outputs, cmap=cmap, norm=norm)
        axis[1, i].set_title(f"y_train {i}")
        axis[1, i].grid(axis="both", color="white", linewidth=1)
        axis[1, i].set_yticks(np.arange(-0.5, outputs.shape[0], 1))
        axis[1, i].set_xticks(np.arange(-0.5, outputs.shape[1], 1))
        axis[1, i].set_yticklabels([])
        axis[1, i].set_xticklabels([])

    inputs = np.array(x.grid)
    axis[0, nb_examples].imshow(inputs, cmap=cmap, norm=norm)
    axis[0, nb_examples].set_title("x_test")
    axis[0, nb_examples].grid(axis="both", color="white", linewidth=1)
    axis[0, nb_examples].set_yticks(np.arange(-0.5, inputs.shape[0], 1))
    axis[0, nb_examples].set_xticks(np.arange(-0.5, inputs.shape[1], 1))
    axis[0, nb_examples].set_yticklabels([])
    axis[0, nb_examples].set_xticklabels([])

    if y_true:
        outputs = np.array(y_true.grid)
        title = "y_true"
    if y_pred:
        outputs = np.array(y_pred.grid)
        title = "y_pred"
    axis[1, nb_examples].imshow(outputs, cmap=cmap, norm=norm)
    axis[1, nb_examples].set_title(title)
    axis[1, nb_examples].grid(axis="both", color="white", linewidth=1)
    axis[1, nb_examples].set_yticks(np.arange(-0.5, outputs.shape[0], 1))
    axis[1, nb_examples].set_xticks(np.arange(-0.5, outputs.shape[1], 1))
    axis[1, nb_examples].set_yticklabels([])
    axis[1, nb_examples].set_xticklabels([])

    plt.tight_layout()
    plt.savefig(to_file)
    plt.close()
    try:
        from IPython import display

        return display.Image(filename=to_file)
    except ImportError:
        pass


@synalinks_export("synalinks.datasets.arcagi.load_data")
def load_data(task_names=None):
    """
    Load and format data from github

    Example:

    ```python
    (x_train, y_train), (x_test, y_test) = synalinks.datasets.arcagi.load_data()
    ```

    Args:
        task_names (list): Optional. The list of tasks to fetch.

    Returns:
        (tuple): The train and test data ready for training
    """
    x_train = []
    y_train = []
    x_test = []
    y_test = []

    if not task_names:
        for task_name in TRAINING_TASK_NAMES:
            (x, y) = fetch_and_format(task_name)
            x_train.append(x)
            y_train.append(y)

        for task_name in EVALUATION_TASK_NAMES:
            (x, y) = fetch_and_format(task_name)
            x_test.append(x)
            y_test.append(y)

    else:
        for task_name in task_names:
            if task_name in TRAINING_TASK_NAMES:
                (x, y) = fetch_and_format(task_name)
                x_train.append(x)
                y_train.append(y)

            if task_name in EVALUATION_TASK_NAMES:
                (x, y) = fetch_and_format(task_name)
                x_test.append(x)
                x_test.append(y)

    x_train = np.array(x_train, dtype="object")
    y_train = np.array(y_train, dtype="object")
    x_test = np.array(x_test, dtype="object")
    y_test = np.array(y_test, dtype="object")

    return (x_train, y_train), (x_test, y_test)


@synalinks_export("synalinks.datasets.arcagi.fetch_and_format")
def fetch_and_format(task_name):
    """
    Fetch and format one task by name

    Example:

    ```python
    x, y = synalinks.datasets.arcagi.fetch_and_format("62c24649")
    ```
    """
    if task_name in TRAINING_TASK_NAMES:
        url = f"{BASE_URL}/training/{task_name}.json"
    elif task_name in EVALUATION_TASK_NAMES:
        url = f"{BASE_URL}/evaluation/{task_name}.json"
    else:
        raise ValueError(
            f"Task '{task_name}' not recognized, make sure that the task name is valid."
        )

    x = None
    y = None

    file_path = file_utils.get_file(origin=url, progbar=False)
    with open(file_path, "r") as f:
        json_data = json.loads(f.read())
        trainset = json_data.get("train")
        testset = json_data.get("test")
        x = ARCAGIInput(grid=testset[0].get("input"))
        x.examples.append(
            TaskExample(
                inputs=tuple(map(tuple, trainset[0].get("input"))),
                outputs=tuple(map(tuple, trainset[0].get("output"))),
            )
        )
        x.examples.append(
            TaskExample(
                inputs=tuple(map(tuple, trainset[1].get("input"))),
                outputs=tuple(map(tuple, trainset[1].get("output"))),
            )
        )
        if len(trainset) > 2:
            x.examples.append(
                TaskExample(
                    inputs=tuple(map(tuple, trainset[2].get("input"))),
                    outputs=tuple(map(tuple, trainset[2].get("output"))),
                )
            )
        y = ARCAGIOutput(grid=tuple(map(tuple, testset[0].get("output"))))
    return x, y
