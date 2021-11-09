import uvicorn
import fastapi
from database import database, table
from typing import List
from patient_model import Patient, PatientIn

app = fastapi.FastAPI(title="BostonGene simple API")
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.diconnect()

@app.get("/")
async def root():
    '''return db size'''

    query = table.select()
    res = await database.fetch_all(query)
    return {"size_db": len(res)}


@app.get("/patients", response_model=List[Patient])
async def read_notes():
    query = table.select()
    return await database.fetch_all(query)


@app.get("/patients/{index}", response_model=Patient)
async def read_notes_by_index(index: int):
    query = table.select().where(table.c.index == index)
    return await database.fetch_one(query=query)

@app.get("/{name}")
async def read_notes_name(name: str):
    query = table.select().where(table.c.nsclc_name == name)
    return await database.fetch_one(query=query)


@app.post("/patients", response_model=Patient)
async def create_note(patient: PatientIn = fastapi.Depends()):
    query = table.select()
    res = await database.fetch_all(query)
    query = table.insert().values(
        index=len(res),
        nsclc_name=patient.nsclc_name,
        mhci=patient.mhci,
        mhcii=patient.mhcii,
        coactivation_molecules=patient.coactivation_molecules,
        effector_cells=patient.effector_cells,
        t_cell_traffic=patient.t_cell_traffic,
        nk_cells=patient.nk_cells,
        t_cells=patient.t_cells,
        b_cells=patient.b_cells,
        m1_signatures=patient.m1_signatures,
        th1_signature=patient.th1_signature,
        antitumor_cytokines=patient.antitumor_cytokines,
        checkpoint_inhibition=patient.checkpoint_inhibition,
        treg=patient.treg,
        t_reg_traffic=patient.t_reg_traffic,
        neutrophil_signature=patient.neutrophil_signature,
        granulocyte_traffic=patient.granulocyte_traffic,
        mdsc=patient.mdsc,
        mdsc_traffic=patient.mdsc_traffic,
        macrophages=patient.macrophages,
        macrophage_dc_traffic=patient.macrophage_dc_traffic,
        th2_signature=patient.th2_signature,
        protumor_cytokines=patient.protumor_cytokines,
        caf=patient.caf,
        matrix=patient.matrix,
        matrix_remodeling=patient.matrix_remodeling,
        angiogenesis=patient.angiogenesis,
        endothelium=patient.endothelium,
        proliferation_rate=patient.proliferation_rate,
        emt_signature=patient.emt_signature
        )
    last_index = await database.execute(query)
    query = table.select().where(table.c.index == len(res))
    res = await database.fetch_one(query)
    return {**res}

@app.put('/change/{index}', response_model=Patient)
async def update(index: int, patient: PatientIn = fastapi.Depends()):
    query = table.select()
    res = await database.fetch_all(query)
    query = table.update().where(table.c.index == index).values(
        index=index,
        nsclc_name=patient.nsclc_name,
        mhci=patient.mhci,
        mhcii=patient.mhcii,
        coactivation_molecules=patient.coactivation_molecules,
        effector_cells=patient.effector_cells,
        t_cell_traffic=patient.t_cell_traffic,
        nk_cells=patient.nk_cells,
        t_cells=patient.t_cells,
        b_cells=patient.b_cells,
        m1_signatures=patient.m1_signatures,
        th1_signature=patient.th1_signature,
        antitumor_cytokines=patient.antitumor_cytokines,
        checkpoint_inhibition=patient.checkpoint_inhibition,
        treg=patient.treg,
        t_reg_traffic=patient.t_reg_traffic,
        neutrophil_signature=patient.neutrophil_signature,
        granulocyte_traffic=patient.granulocyte_traffic,
        mdsc=patient.mdsc,
        mdsc_traffic=patient.mdsc_traffic,
        macrophages=patient.macrophages,
        macrophage_dc_traffic=patient.macrophage_dc_traffic,
        th2_signature=patient.th2_signature,
        protumor_cytokines=patient.protumor_cytokines,
        caf=patient.caf,
        matrix=patient.matrix,
        matrix_remodeling=patient.matrix_remodeling,
        angiogenesis=patient.angiogenesis,
        endothelium=patient.endothelium,
        proliferation_rate=patient.proliferation_rate,
        emt_signature=patient.emt_signature
    )
    await database.execute(query)
    query = table.select().where(table.c.index == index)
    res = await database.fetch_one(query)
    return {**res}

@app.delete("/delete/{index}", response_model=Patient)
async def delete(index: int):
    query = table.delete().where(table.c.index == index)
    return await database.execute(query)

if __name__ == '__main__':
    uvicorn.run("main:app",port=8000, host="0.0.0.0", reload=True)