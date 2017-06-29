#include <memory>
#include <iostream>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

class Simple_Plots : public edm::one::EDAnalyzer<>  {
   public:
      explicit Simple_Plots(const edm::ParameterSet&);
   private:
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<GenEventInfoProduct> MyGenEventInfoProduct_;
};


//
Simple_Plots::Simple_Plots(const edm::ParameterSet& iConfig){  
  //MyGenEventInfoProduct_ = consumes<GenEventInfoProduct>( iConfig.getParameter<edm::InputTag>("genSource") );
  MyGenEventInfoProduct_ = consumes<GenEventInfoProduct>( edm::InputTag("generator") );}

// ------------ method called for each event  ------------
void
Simple_Plots::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  edm::Handle<GenEventInfoProduct> GenEventInfo;
  iEvent.getByToken(MyGenEventInfoProduct_, GenEventInfo);
  std::cout<<GenEventInfo->weight()<<std::endl;}
DEFINE_FWK_MODULE(Simple_Plots);
