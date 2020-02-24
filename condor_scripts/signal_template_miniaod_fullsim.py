import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
#------ Setup ------#

#initialize the process
process = cms.Process("LLPNtupler")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff")
process.load("Configuration.EventContent.EventContent_cff")

#load input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'file:/mnt/hadoop/store/group/phys_exotica/jmao/aodsim/RunIISummer16/AODSIM/MSSM-1d-prod/n3n2-n1-hbb-hbb_mh200_pl100_ev100000/crab_CMSSW_8_0_21_n3n2-n1-hbb-hbb_mchi200_pl100_ev100000_AODSIM_CaltechT2/190912_202259/0000/n3n2-n1-hbb-hbb_step2_10.root',
)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

#TFileService for output
process.TFileService = cms.Service("TFileService",
	fileName = cms.string('ntuple_RunIISummer16_x1n2_wlv_hbb_pl10000.root'),
    closeFileFast = cms.untracked.bool(True)
)

#load run conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

#------ Declare the correct global tag ------#


#process.GlobalTag.globaltag = '94X_mc2017_realistic_v17'
process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_v3'

#------ If we add any inputs beyond standard miniAOD event content, import them here ------#

process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')

#------ Analyzer ------#

# For AOD Track variables
process.MaterialPropagator = cms.ESProducer('PropagatorWithMaterialESProducer',
    ComponentName = cms.string('PropagatorWithMaterial'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)

#list input collections
process.ntuples = cms.EDAnalyzer('displacedJetTiming_ntupler',
    isData = cms.bool(False),
    useGen = cms.bool(True),
    isFastsim = cms.bool(False),
    enableTriggerInfo = cms.bool(True),
    enableEcalRechits = cms.bool(False),
    enableCaloJet = cms.bool(False),
    enableGenLLPInfo = cms.bool(True),
    readGenVertexTime = cms.bool(False),#need to be false for displaced samples
    llpId = cms.int32(1023),

    genParticles_t0 = cms.InputTag("genParticles", "t0", ""),
    triggerPathNamesFile = cms.string("cms_lpc_llp/llp_timing_ntupler/data/trigger_names_llp_v1.dat"),
    eleHLTFilterNamesFile = cms.string("SUSYBSMAnalysis/RazorTuplizer/data/RazorElectronHLTFilterNames.dat"),
    muonHLTFilterNamesFile = cms.string("SUSYBSMAnalysis/RazorTuplizer/data/RazorMuonHLTFilterNames.dat"),
    photonHLTFilterNamesFile = cms.string("SUSYBSMAnalysis/RazorTuplizer/data/RazorPhotonHLTFilterNames.dat"),

    vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", "PAT"),
    muons = cms.InputTag("slimmedMuons","","PAT"),
    electrons = cms.InputTag("slimmedElectrons","","PAT"),
    taus = cms.InputTag("slimmedTaus","","PAT"),
    photons = cms.InputTag("slimmedPhotons","","PAT"),
    jetsCalo = cms.InputTag("slimmedJets","","PAT"),
    jets = cms.InputTag("slimmedJets","","PAT"),
    jetsPuppi = cms.InputTag("slimmedJetsPuppi","","PAT"),
    jetsAK8 = cms.InputTag("slimmedJetsAK8","","PAT"),
    mets = cms.InputTag("slimmedMETs","","PAT"),
    metsPuppi = cms.InputTag("slimmedMETsPuppi","","PAT"),

    genParticles = cms.InputTag("genParticles"),

    #genMetsTrue = cms.InputTag("genMetTrue"),
    #genMetsCalo = cms.InputTag("genMetTrue"),
    genJets = cms.InputTag("slimmedGenJets","","PAT"),

    triggerBits = cms.InputTag("TriggerResults","","HLT"),

    metFilterBits = cms.InputTag("TriggerResults", "", "PAT"),

    #hbheNoiseFilter = cms.InputTag("HBHENoiseFilterResultProducer","HBHENoiseFilterResult"),
    #hbheTightNoiseFilter = cms.InputTag("HBHENoiseFilterResultProducer","HBHENoiseFilterResultRun2Tight"),
    #hbheIsoNoiseFilter = cms.InputTag("HBHENoiseFilterResultProducer","HBHEIsoNoiseFilterResult"),

    #BadChargedCandidateFilter = cms.InputTag("BadChargedCandidateFilter",""),
    #BadMuonFilter = cms.InputTag("BadPFMuonFilter",""),

    genInfo = cms.InputTag("generator", "", "SIM"),

    tracks = cms.InputTag("isolatedTracks", "", "PAT"),

    puInfo = cms.InputTag("slimmedAddPileupInfo", "", "PAT"), #uncomment if no pre-mixing

    secondaryVertices = cms.InputTag("slimmedSecondaryVertices","", "PAT"),

    rhoAll = cms.InputTag("fixedGridRhoAll", "", "RECO"),

    rhoFastjetAll = cms.InputTag("fixedGridRhoFastjetAll", "", "RECO"),
    rhoFastjetAllCalo = cms.InputTag("fixedGridRhoFastjetAllCalo", "", "RECO"),
    rhoFastjetCentralCalo = cms.InputTag("fixedGridRhoFastjetCentralCalo", "", "RECO"),
    rhoFastjetCentralChargedPileUp = cms.InputTag("fixedGridRhoFastjetCentralChargedPileUp", "", "RECO"),
    rhoFastjetCentralNeutral = cms.InputTag("fixedGridRhoFastjetCentralNeutral", "", "RECO"),

    beamSpot = cms.InputTag("offlineBeamSpot", "", "RECO"),
    #pfClusters = cms.InputTag("particleFlowClusterECAL","","PAT"),
    ebRecHits = cms.InputTag("reducedEgamma", "reducedEBRecHits", "PAT"),
    eeRecHits  = cms.InputTag("reducedEgamma", "reducedEERecHits", "PAT"),
    esRecHits = cms.InputTag("reducedEgamma", "reducedESRecHits", "PAT"),
    ebeeClusters = cms.InputTag("reducedEgamma", "reducedEBEEClusters", "PAT"),
    esClusters = cms.InputTag("reducedEgamma", "reducedESClusters", "PAT"),
    conversions = cms.InputTag("reducedEgamma", "reducedConversions", "PAT"),
    singleLegConversions = cms.InputTag("reducedEgamma", "reducedSingleLegConversions", "PAT"),

    gedGsfElectronCores = cms.InputTag("reducedEgamma", "reducedGedGsfElectronCores", "PAT"),
    gedPhotonCores = cms.InputTag("reducedEgamma", "reducedGedPhotonCores", "PAT"),
    #generaltracks = cms.InputTag("isolatedTracks", "", "PAT"),
    #superClusters = cms.InputTag("reducedEgamma", "reducedSuperClusters", "PAT"),

    #lostTracks = cms.InputTag("lostTracks", "", "PAT")
)

#run
process.p = cms.Path( process.ntuples)
